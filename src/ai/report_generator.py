from dotenv import load_dotenv
import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.ai.rag_engine import RAGEngine

# Load environment variables from .env
load_dotenv()

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, provider: str = "google", model_name: str = "gemini-flash-latest", api_key: str = None):
        """
        Initializes the LLM report generator with multiple provider support.
        :param provider: 'google' or 'openai'
        :param model_name: Name of the model (e.g., 'gemini-1.5-flash' or 'gpt-4o')
        :param api_key: Optional API key (overrides environment variable)
        """
        # If no key is provided, try to get it from environment
        if not api_key:
            if provider == "google":
                api_key = os.getenv("GOOGLE_API_KEY", "").strip()
            elif provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY", "").strip()

        if provider == "google":
            self.llm = ChatGoogleGenerativeAI(
                model=model_name, 
                temperature=0.2,
                google_api_key=api_key if api_key else None
            )
        elif provider == "openai":
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=0.2,
                api_key=api_key if api_key else None
            )
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")

        self.rag = RAGEngine()
        
    def generate_report(
        self, 
        symbol: str, 
        strategy_name: str, 
        tech_reason: str, 
        current_price: float, 
        metrics: dict = None, 
        language: str = "English",
        macro_context: dict = None,
        news_items: list = None
    ) -> str:
        """Groups RAG knowledge with technical findings to provide a summary in the selected language."""
        
        # Consult the RAG knowledge base for user criteria
        user_knowledge = self.rag.similarity_search(f"Investment criteria and risk factors for {strategy_name} in stocks", k=3)
        
        # Ensure default empty dictionary for metrics
        metrics = metrics or {}

        # Macro context
        if macro_context:
            macro_text = (
                f"S&P 500: {macro_context.get('SPY',{}).get('change_pct',0):+.2f}% | "
                f"Nasdaq: {macro_context.get('QQQ',{}).get('change_pct',0):+.2f}% | "
                f"VIX: {macro_context.get('VIX',{}).get('value','N/A')} "
                f"({'HIGH VOLATILITY' if macro_context.get('alerta_vix') else 'normal'}) | "
                f"10Y Bond: {macro_context.get('TNX',{}).get('value','N/A')}%"
            )
        else:
            macro_text = "Market context not available."

        # News context
        if news_items:
            news_text = "\n".join([
                f"- [{n['source']}] {n['headline']} — {n['summary']}"
                for n in news_items[:5]
            ])
        else:
            news_text = ("No real-time news available. "
                         "Section based on model training knowledge only.")
        
        prompt = PromptTemplate.from_template("""
You are a swing trading analyst acting as a sanity
check. The technical system has detected a potential
opportunity. Your job: find reasons NOT to enter,
or confirm the thesis is clean.

Keep it under 400 words. Be specific. No generic advice.

═══════════════════════════════════
TECHNICAL SIGNAL:
═══════════════════════════════════
Ticker: {symbol} | Price: ${current_price}
Pattern: {bucket}{subtype_str}
Phase: {phase} ({progress_pct}% of recovery)
Upside to ATH 3Y: {upside_to_ath3y}%
Drop: {drop_pct}% | Rebound: {rebound_pct}%
RSI(14): {rsi_14} | Volume vs 3M: {vol_ratio_3m}x
Price movement structure: {era_sequence}

═══════════════════════════════════
MARKET CONTEXT TODAY:
═══════════════════════════════════
{macro_context_text}

═══════════════════════════════════
COMPANY FUNDAMENTALS (yfinance):
═══════════════════════════════════
Market Cap: {market_cap}B | P/E: {per} | EPS: {eps}
Dividend: {dividend_yield}% | Next Earnings: {next_earnings}
Volume: {volume}M avg

═══════════════════════════════════
RECENT NEWS ({news_source}):
═══════════════════════════════════
{news_text}

═══════════════════════════════════
YOUR INVESTMENT CRITERIA (RAG):
═══════════════════════════════════
{user_knowledge}

═══════════════════════════════════
REPORT STRUCTURE:
═══════════════════════════════════

## ⚡ Verdict
[ENTER / WAIT / AVOID] — One sentence.

## 🚨 Risk Flags
List only real risks that invalidate the thesis.
If none: "No critical flags detected."
Auto-flags to always check:
- If next_earnings < 14 days: mention gap risk
- If RSI > 75: mention overbought chase risk
- If phase is LATE and upside < 5%: flag low upside
- If vol_ratio < 0.5: flag low conviction

## 📰 News & Sentiment
Tone: [Positive/Neutral/Negative/Unknown]
Key themes: (1-2 lines, specific to {symbol})
{news_disclaimer}

## 💡 One thing to check manually
The single most important thing to verify on Yahoo
Finance or SEC before entering.

## ✅ Thesis Summary
If verdict is ENTER or WAIT: confirm why the
technical signal makes sense fundamentally in 2-3
lines.

---
Rules:
- Earnings < 7 days → verdict WAIT minimum
- RAG contradicts entry → verdict AVOID
- Respond in {language}
""")
        
        subtype_str = (f" → {metrics.get('subtype','')}" if metrics.get('subtype') else "")
        news_disclaimer = ("" if news_items else "⚠️ Based on model training data, not real-time.")
        news_source = ("Finnhub real-time" if news_items else "model knowledge")

        formatted_prompt = prompt.format(
            symbol=symbol,
            current_price=metrics.get("current_price", current_price),
            bucket=metrics.get("bucket", "N/A"),
            subtype_str=subtype_str,
            phase=metrics.get("phase", "N/A"),
            progress_pct=round(metrics.get("progress_pct", 0) or 0, 0),
            upside_to_ath3y=round(metrics.get("upside_to_ath3y", 0) or 0, 1),
            drop_pct=round(metrics.get("drop_from_high_pct") or metrics.get("drop_pct", 0) or 0, 1),
            rebound_pct=round(metrics.get("rebound_pct", 0) or 0, 1),
            rsi_14=metrics.get("rsi_14", "N/A"),
            vol_ratio_3m=metrics.get("vol_ratio_3m", "N/A"),
            era_sequence=metrics.get("era_sequence", []),
            macro_context_text=macro_text,
            market_cap=round(metrics.get("market_cap", 0) or 0, 1),
            per=metrics.get("per", "N/A"),
            eps=metrics.get("eps", "N/A"),
            dividend_yield=metrics.get("dividend_yield", "N/A"),
            next_earnings=metrics.get("next_earnings", "N/A"),
            volume=round(metrics.get("volume", 0) or 0, 1),
            news_text=news_text,
            news_source=news_source,
            news_disclaimer=news_disclaimer,
            user_knowledge=user_knowledge,
            language=language,
            strategy_name=strategy_name,
            tech_reason=tech_reason
        )
        
        import time
        for attempt in range(2): # Try twice
            try:
                response = self.llm.invoke(formatted_prompt)
                content = response.content
                if isinstance(content, list):
                    # Concatenate all text parts if the response is a list
                    content = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
                return content
            except Exception as e:
                err_msg = str(e).lower()
                if "resource_exhausted" in err_msg or "429" in err_msg:
                    if attempt == 0:
                        logger.warning(f"Rate limit hit for {symbol}. Retrying in 15s...")
                        time.sleep(15)
                        continue
                    else:
                        return f"Error: API Quota Exceeded (429). You are on a Free Tier and have exceeded the limits for this model. Please wait a minute or switch to 'gemini-flash-latest' which has higher limits."
                
                logger.error(f"Error invoking LLM for reports: {e}")
                return f"Error from AI generating the report ({e}). Check if your Google API Key is valid."
        return "Critical: Failed to generate report after retries."
        return "Critical: Failed to generate report after retries."
