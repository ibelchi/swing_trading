import streamlit as st
import pandas as pd
import tempfile
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load and configure Google AI at the very beginning
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path)

api_key = os.getenv("GOOGLE_API_KEY", "").strip()
if api_key:
    genai.configure(api_key=api_key)
    os.environ["GOOGLE_API_KEY"] = api_key

from src.database.db import SessionLocal, Opportunity, StrategyConfig, get_db
from src.scanner.market_scanner import MarketScanner
from src.ui.opportunity_chart import render_opportunity_chart
from src.ai.rag_engine import RAGEngine
from src.ai.report_generator import ReportGenerator
from src.data.ingestion import get_company_info, get_historical_data

# --- PAGE CONFIG ---
st.set_page_config(page_title="RadarCore", layout="wide")
st.title("📡 RadarCore")

# --- CUSTOM THEME (Purple & Red) ---
st.markdown("""
<style>
    /* Primary buttons as Pastel Purple/Lavender */
    div.stButton > button:first-child {
        background-color: #9b59b6;
        color: white;
        border-radius: 5px;
        border: 1px solid #000000;
    }
    div.stButton > button:first-child:hover {
        background-color: #8e44ad;
        color: white;
        border: 1px solid #000000;
    }
    /* Specific styling for the Delete button (Danger) */
    div.stButton > button[kind="secondary"] {
        background-color: #e74c3c;
        color: white;
        border-radius: 5px;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #c0392b;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("Global Settings")
    st.subheader("AI Configuration")
    ai_provider = st.radio("AI Provider", ["Google Gemini", "OpenAI"], index=0)
    
    if ai_provider == "Google Gemini":
        models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]
    else:
        models = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
        
    ai_model = st.selectbox("Model", models, index=0)
    
    # Optional API Key override
    with st.expander("API Key Settings (Optional)"):
        user_api_key = st.text_input(f"Override {ai_provider} API Key", type="password")
        if user_api_key:
            st.caption(f"🔑 Specific {ai_provider} key will be used.")

    st.divider()

    report_lang = st.selectbox(
        "AI Report Language",
        ["Catalan", "Spanish", "English"],
        index=0,
        help="Select the language for the AI-generated research reports."
    )

# --- TABS ---
tab_config, tab_scanner, tab_history, tab_knowledge = st.tabs([
    "⚙️ Strategy Settings",
    "🔍 Market Scanner", 
    "📚 History & Reports", 
    "🧠 Investor Knowledge (RAG)"
])

# --- TAB SCANNER ---
with tab_scanner:
    st.header("Daily Market Scanning")
    st.write("Find opportunities based on active swing trading strategies.")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        market_options = {
            "S&P 500 (USA)": "sp500",
            "NASDAQ 100 (USA)": "nasdaq100",
            "IBEX 35 (Spain)": "ibex35",
            "DAX 40 (Germany)": "dax40",
            "EuroStoxx 50 (Europe)": "eurostoxx50",
            "Nikkei 225 (Japan)": "nikkei225",
            "Nifty 50 (India)": "nifty50"
        }
        market_choice = st.selectbox("Market to Scan:", list(market_options.keys()))
        market_key = market_options[market_choice]
        
        if market_key in ["sp500", "ibex35", "dax40", "eurostoxx50", "nifty50"]:
            st.caption("ℹ️ Internal fixed list/stable source for stability. Last review: **April 2026**.")
        else:
            st.caption("🟢 **Live** scanning against internet directories.")
            
        limit = st.number_input("Symbol limit (0 for full market)", min_value=0, max_value=4000, value=0)
        start_btn = st.button("Run Scanner", type="primary")
        
    with col2:
        if start_btn:
            with st.spinner(f"Scanning {market_choice} market... This may take a while"):
                scanner = MarketScanner()
                with st.status("Scanning in progress...", expanded=True) as status:
                    st.write("Checking market symbols and downloading SPY context...")
                    
                    results_container = st.container()
                    
                    def live_chart_callback(symbol, hist, result):
                        with results_container:
                            st.success(f"New Opportunity Found: {symbol}")
                            with st.expander(f"📈 View Analysis Chart — {symbol}", expanded=True):
                                render_opportunity_chart(symbol, hist, result["metrics"])
                    
                    try:
                        scanner.run_scan(
                            market=market_key, 
                            limit_symbols=limit if limit > 0 else None,
                            on_opportunity_found=live_chart_callback
                        )
                        status.update(label="Scan completed!", state="complete", expanded=False)
                        st.success("Scan finished! New opportunities have been saved to History.")
                    except Exception as e:
                        st.error(f"⚠️ Critical error during scan: {e}")

# --- TAB HISTORY ---
with tab_history:
    st.header("Detected Opportunities")
    db = SessionLocal()
    
    # Auto-migration for confidence column
    try:
        from sqlalchemy import text
        db.execute(text("ALTER TABLE opportunities ADD COLUMN confidence FLOAT"))
        db.commit()
    except Exception:
        db.rollback() # Column likely already exists
        
    try:
        opportunities = db.query(Opportunity).order_by(Opportunity.date_detected.desc()).limit(50).all()
        if not opportunities:
            st.info("No market opportunities detected yet.")
        else:
            # Display summary table with Yahoo Finance links
            def fmt_curr(price, curr_code):
                symbols = {"EUR": "€", "USD": "$", "JPY": "¥", "INR": "₹", "GBP": "£"}
                s = symbols.get(curr_code, curr_code or "$")
                return f"{price:.2f} {s}"

            data = []
            for op in opportunities:
                # Resolve technical metrics
                m = op.metrics or {}
                drop_val = m.get("drop_from_high_pct") or m.get("drop_pct", 0)
                rebound_val = m.get("rebound_pct", 0)
                pattern = m.get("pattern_type", "N/A")
                # Defensive check for confidence (might not exist in old DBs)
                confidence = getattr(op, 'confidence', 0.0) or 0.0

                data.append({
                    "Symbol": f"https://es.finance.yahoo.com/quote/{op.symbol}/",
                    "Company": op.company_name or op.symbol,
                    "Drop %": f"{drop_val:.2f}%",
                    "Rebound %": f"{rebound_val:.2f}%",
                    "Pattern": pattern,
                    "Conf.": f"{confidence:.1f}%",
                    "Market": op.market.upper() if op.market else "S&P500",
                    "Date": op.date_detected.strftime('%Y-%m-%d'),
                    "_symbol_real": op.symbol, # For lookups
                })
            
            df = pd.DataFrame(data)
            
            # Action Buttons Row
            col_down, col_del = st.columns([1, 1])
            with col_down:
                # CSV Export Logic remains mostly same, just cleaner
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Full History (CSV)",
                    data=csv_data,
                    file_name="radarcore_history.csv",
                    mime="text/csv"
                )
            with col_del:
                if st.button("🗑️ Delete All History", type="secondary"):
                    db_del = SessionLocal()
                    try:
                        db_del.query(Opportunity).delete()
                        db_del.commit()
                        st.warning("History cleared!")
                        st.rerun()
                    finally:
                        db_del.close()

            df = df.sort_values(by="Symbol") # Alphabetical sorting
            
            st.dataframe(
                df.drop(columns=["_symbol_real"]),
                column_config={
                    "Symbol": st.column_config.LinkColumn(
                        "Symbol",
                        display_text=r"https://es\.finance\.yahoo\.com/quote/(.*?)/"
                    )
                },
                use_container_width=True,
                hide_index=True
            )
            
            st.divider()
            st.subheader("Visual Analysis & Reports")
            
            # Detailed Analysis with Charts
            for op in opportunities:
                with st.expander(f"📈 {op.symbol} — {op.company_name or op.symbol} ({op.date_detected.strftime('%Y-%m-%d')})"):
                    col_info, col_chart = st.columns([1, 3])
                    with col_info:
                        st.write(f"**Strategy:** {op.strategy_name}")
                        st.write(f"**Signal Price:** ${op.current_price:.2f}")
                        st.write(f"**Market:** {op.market}")
                        if st.button(f"Generate AI Report", key=f"btn_rep_{op.id}"):
                            st.info("AI Report generation logic would go here.")
                    
                    with col_chart:
                        # Lazy load historical data for the chart
                        with st.spinner(f"Loading chart for {op.symbol}..."):
                            # Fetch 2y to ensure we cover the period_high/low context
                            h_data = get_historical_data(op.symbol, period="2y")
                            if not h_data.empty:
                                render_opportunity_chart(op.symbol, h_data, op.metrics)
                            else:
                                st.error("Could not fetch historical data for chart.")
            
            st.divider()
            st.subheader("🔍 On-Demand Research")
            st.write("Analyze any ticker immediately or select from history.")

            c1, c2 = st.columns([1, 4])
            with c1:
                # Part 1: Manual Search
                manual_ticker = st.text_input("Enter Ticker (e.g., TSLA, SAN.MC):").upper()
                if st.button("Research Ticker", type="primary"):
                    if not manual_ticker:
                        st.warning("Please enter a valid ticker.")
                    else:
                        with st.spinner(f"Analyzing {manual_ticker}..."):
                            try:
                                info = get_company_info(manual_ticker)
                                hist = get_historical_data(manual_ticker)
                                if hist.empty:
                                    st.error("No data found.")
                                else:
                                    curr_p = hist['Close'].iloc[-1]
                                    h60, l60 = hist['High'].tail(60).max(), hist['Low'].tail(60).min()
                                    metrics = {
                                        "current_price": curr_p, "period_high": h60, "period_low": l60,
                                        "drop_pct": ((h60 - curr_p) / h60) * 100, "rebound_pct": ((curr_p - l60) / l60) * 100,
                                        "lookback_days": 60, "market_cap": info.get("market_cap", 0) / 1e9,
                                        "volume": hist['Volume'].tail(10).mean() / 1e6,
                                        "per": info.get("per", "N/A"), "eps": info.get("eps", "N/A"),
                                        "dividend_yield": info.get("dividend_yield", "N/A"), "next_earnings": info.get("next_earnings", "N/A")
                                    }
                                    gen = ReportGenerator(
                                        provider=provider_key, 
                                        model_name=ai_model, 
                                        api_key=user_api_key if user_api_key else None
                                    )
                                    report = gen.generate_report(manual_ticker, "Direct Search", "User Request", curr_p, metrics, language=report_lang)
                                    
                                    # Save to reports/ folder
                                    os.makedirs("reports", exist_ok=True)
                                    filename = f"reports/radarcore_report_{manual_ticker}_{pd.Timestamp.now().strftime('%y%m%d')}.md"
                                    with open(filename, "w", encoding="utf-8") as f:
                                        f.write(report)
                                    
                                    st.session_state['manual_report'] = report
                                    st.session_state['manual_ticker_status'] = manual_ticker
                                    st.session_state['manual_report_file'] = filename
                            except Exception as e:
                                st.error(f"Error: {e}")

                st.divider()
                
                # Part 2: Multiselect from History
                ticker_list = sorted(df["_symbol_real"].unique().tolist()) # Alphabetical sorting
                selected_symbols = st.multiselect("Select from History", ticker_list)
                
                if st.button("Generate Selected", type="primary"):
                    if not selected_symbols:
                        st.warning("Select symbols.")
                    else:
                        all_reports = ""
                        progress_bar = st.progress(0)
                        for idx, sym in enumerate(selected_symbols):
                            with st.status(f"Analyzing {sym}...", expanded=True) as status:
                                op = db.query(Opportunity).filter(Opportunity.symbol == sym).order_by(Opportunity.date_detected.desc()).first()
                                if op:
                                    gen = ReportGenerator(
                                        provider=provider_key, 
                                        model_name=ai_model, 
                                        api_key=user_api_key if user_api_key else None
                                    )
                                    report_content = gen.generate_report(op.symbol, op.strategy_name, op.explanation, op.current_price, op.metrics, language=report_lang)
                                    
                                    # Save each individually to reports/
                                    os.makedirs("reports", exist_ok=True)
                                    fname = f"reports/radarcore_report_{op.symbol}_{pd.Timestamp.now().strftime('%y%m%d')}.md"
                                    with open(fname, "w", encoding="utf-8") as f:
                                        f.write(report_content)
                                        
                                    st.markdown(f"### Report: {sym}")
                                    st.markdown(report_content)
                                    all_reports += f"# MARKET REPORT: {sym}\n\n{report_content}\n\n---\n\n"
                                progress_bar.progress((idx + 1) / len(selected_symbols))
                                status.update(label=f"Analysis of {sym} completed", state="complete")
                        
                        st.divider()
                        st.download_button(
                            label="📥 Download all reports (.md)",
                            data=all_reports,
                            file_name="radarcore_reports.md",
                            mime="text/markdown"
                        )
            
            with c2:
                if 'manual_report' in st.session_state:
                    st.markdown(f"### Research Report: {st.session_state['manual_ticker_status']}")
                    st.markdown(st.session_state['manual_report'])
                    st.download_button(
                        label=f"📥 Download {st.session_state['manual_ticker_status']} Report",
                        data=st.session_state['manual_report'],
                        file_name= f"radarcore_report_{st.session_state['manual_ticker_status']}_{pd.Timestamp.now().strftime('%y%m%d')}.md",
                        mime="text/markdown"
                    )
    finally:
        db.close()

# --- TAB CONFIG ---
with tab_config:
    st.header("Strategy Configuration")
    st.write("Adjust strategy parameters without touching the code.")
    
    # Direct import trick
    from src.strategies.buy_the_dip import BuyTheDipStrategy
    btd = BuyTheDipStrategy()
    
    db = SessionLocal()
    try:
        conf_record = db.query(StrategyConfig).filter(StrategyConfig.strategy_name == btd.name).first()
        actual_params = conf_record.parameters if conf_record else btd.default_parameters
        
        with st.form("btd_config"):
            st.subheader(btd.name)
            
            col1, col2 = st.columns(2)
            with col1:
                min_drop = st.slider("Minimum Drop (%)", 5.0, 50.0, actual_params.get("min_drop_pct", 15.0), 0.5)
                lookback = st.slider("Historical Window (Days)", 20, 250, actual_params.get("lookback_days", 60), 5)
                min_rebound = st.slider("Minimum Rebound (%)", 0.0, 15.0, actual_params.get("min_rebound_pct", 2.0), 0.5)
            
            with col2:
                mc = st.number_input("Min Market Cap (B $)", 0.0, 1000.0, actual_params.get("min_market_cap_b", 10.0))
                vol = st.number_input("Min Average Volume (M)", 0.0, 100.0, actual_params.get("min_volume_m", 1.0))
                
            guardar = st.form_submit_button("Save Changes")
            if guardar:
                new_p = {
                    "min_drop_pct": min_drop,
                    "lookback_days": lookback,
                    "min_rebound_pct": min_rebound,
                    "min_market_cap_b": mc,
                    "min_volume_m": vol
                }
                if not conf_record:
                    conf_record = StrategyConfig(strategy_name=btd.name, parameters=new_p)
                    db.add(conf_record)
                else:
                    conf_record.parameters = new_p
                db.commit()
                st.success("Configuration saved and applied for the next scan.")
    finally:
        db.close()

# --- TAB KNOWLEDGE (RAG) ---
with tab_knowledge:
    st.header("Investor Knowledge Base")
    st.write("Upload books, methods, or notes to educate the AI for your reports.")
    
    pdf_docs = st.file_uploader("Upload PDF books here", accept_multiple_files=True, type=['pdf'])
    if st.button("Process & Inject Knowledge"):
        if pdf_docs:
            with st.spinner("Fragmenting and vectorizing (FAISS + Google Embeddings)..."):
                eng = RAGEngine()
                for pdf_file in pdf_docs:
                    # Save temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(pdf_file.getvalue())
                        tmp_path = tmp.name
                    
                    ok = eng.process_pdf(tmp_path)
                    os.unlink(tmp_path)
                    
                    if ok:
                        st.success(f"Document '{pdf_file.name}' indexed successfully.")
                    else:
                        st.error(f"Failed to index '{pdf_file.name}'.")
        else:
            st.warning("Please select at least one document.")
