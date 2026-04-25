from datetime import datetime
import json

def classify_opportunity(opp) -> str:
    """
    Retorna: "top_pick", "on_watch",
             "with_flags" o "skip_today"
    """
    m = getattr(opp, "metrics", {}) or (opp.get("metrics", {}) if isinstance(opp, dict) else {})
    phase = m.get("phase", "")
    rsi = m.get("rsi_14", 50)
    if rsi is None: rsi = 50
    upside = m.get("upside_to_ath3y", 0)
    if upside is None: upside = 0
    days_earn = m.get("days_to_next_earnings")
    
    # Handle the not_recommended flag
    not_rec = False
    if isinstance(opp, dict):
        not_rec = opp.get("not_recommended", False)
    else:
        not_rec = getattr(opp, "not_recommended", False)

    if not_rec or phase == "LATE":
        return "skip_today"

    has_flags = (
        rsi > 70 or
        upside < 5 or
        (days_earn is not None and days_earn < 14)
    )
    if has_flags:
        return "with_flags"

    is_top = (
        phase in ("VALLEY", "MID") and
        35 <= rsi <= 65 and
        upside >= 15 and
        (days_earn is None or days_earn >= 14)
    )
    if is_top:
        return "top_pick"

    return "on_watch"

def get_flag_motive(opp) -> str:
    m = getattr(opp, "metrics", {}) or (opp.get("metrics", {}) if isinstance(opp, dict) else {})
    rsi = m.get("rsi_14", 50) or 50
    upside = m.get("upside_to_ath3y", 0) or 0
    days_earn = m.get("days_to_next_earnings")
    
    motives = []
    if rsi > 70: motives.append(f"RSI Overbought ({rsi:.1f})")
    if upside < 5: motives.append(f"Low Upside ({upside:.1f}%)")
    if days_earn is not None and days_earn < 14: motives.append(f"Earnings in {days_earn}d")
    return " | ".join(motives) if motives else "Technical Warning"

def get_skip_reason(opp) -> str:
    m = getattr(opp, "metrics", {}) or (opp.get("metrics", {}) if isinstance(opp, dict) else {})
    phase = m.get("phase", "")
    if phase == "LATE": return "Late Cycle / Mature Extension"
    
    # Try to get reason from analysis_utils
    try:
        from src.utils.analysis_utils import is_not_recommended_today
        _, reason = is_not_recommended_today(m)
        return reason or "Strategy exclusion"
    except:
        return "Excluded by risk filters"

def generate_html_report(
    opportunities: list,
    macro_data: dict = None,
    scan_config: dict = None,
    not_recommended: list = None,
    reports: dict = None  # {symbol: report_text}
) -> str:
    """
    Generates a standalone HTML report for the detected opportunities.
    Re-structured on 2026-04-25 into 4 categories.
    """
    # 1. DEDUPLICATE AND MERGE
    all_opps = []
    seen = set()
    
    # Process recommended
    for opp in opportunities:
        sym = getattr(opp, "symbol", None) or (opp.get("symbol") if isinstance(opp, dict) else None)
        if sym and sym not in seen:
            seen.add(sym)
            # Inject recommendation flag for classifier
            if isinstance(opp, dict): opp["not_recommended"] = False
            else: setattr(opp, "not_recommended", False)
            all_opps.append(opp)
            
    # Process not recommended
    if not_recommended:
        for opp in not_recommended:
            sym = getattr(opp, "symbol", None) or (opp.get("symbol") if isinstance(opp, dict) else None)
            if sym and sym not in seen:
                seen.add(sym)
                if isinstance(opp, dict): opp["not_recommended"] = True
                else: setattr(opp, "not_recommended", True)
                all_opps.append(opp)

    # 2. CLASSIFY
    categories = {
        "top_pick": [],
        "on_watch": [],
        "with_flags": [],
        "skip_today": []
    }
    
    for opp in all_opps:
        cat = classify_opportunity(opp)
        categories[cat].append(opp)

    # 3. SORT
    # Priority: Phase (VALLEY > MID > MATURE) then Upside 3Y desc
    PHASE_PRIORITY = {"VALLEY": 0, "MID": 1, "MATURE": 2, "LATE": 3}
    def sort_key(o):
        m = getattr(o, "metrics", {}) or (o.get("metrics", {}) if isinstance(o, dict) else {})
        p = m.get("phase", "UNKNOWN")
        pv = PHASE_PRIORITY.get(p, 99)
        up = m.get("upside_to_ath3y", 0) or 0
        return (pv, -up)

    for k in categories:
        categories[k].sort(key=sort_key)

    n_top = len(categories["top_pick"])
    n_watch = len(categories["on_watch"])
    n_flags = len(categories["with_flags"])
    n_skip = len(categories["skip_today"])

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # CSS Styles
    css = """
    <style>
    :root {
        --bg: #0b0d10;
        --card-bg: #161b22;
        --card-border: #232a35;
        --text: #e6edf3;
        --text-dim: #848d97;
        --gold: #c9a35c;
        --gold-light: #e8c98e;
        --green: #4ade80;
        --red: #f87171;
        --amber: #fbbf24;
        --blue: #3b82f6;
    }
    
    body {
        background-color: var(--bg);
        color: var(--text);
        font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        margin: 0;
        padding: 40px 20px;
        line-height: 1.5;
    }
    
    .container {
        max-width: 1100px;
        margin: 0 auto;
    }
    
    header {
        text-align: center;
        margin-bottom: 40px;
    }
    
    .pulse-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: var(--red);
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(248, 113, 113, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(248, 113, 113, 0); }
        100% { box-shadow: 0 0 0 0 rgba(248, 113, 113, 0); }
    }
    
    h1 { font-size: 2.2rem; margin-bottom: 5px; }
    .timestamp { color: var(--text-dim); font-size: 0.85rem; }
    
    .summary-bar {
        display: flex; gap: 30px; justify-content: center;
        margin: 20px 0; font-size: 0.9rem;
        color: var(--text-dim);
    }
    .summary-bar span { font-weight: 600; }

    /* Macro Grid */
    .macro-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 15px;
        margin-bottom: 30px;
    }
    
    .macro-tile {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        padding: 12px;
        border-radius: 8px;
        text-align: center;
    }
    
    .macro-label { font-size: 0.75rem; color: var(--text-dim); display: block; }
    .macro-value { font-size: 1.1rem; font-weight: 700; display: block; }
    .macro-change { font-size: 0.8rem; font-weight: 600; }
    .positive { color: var(--green); }
    .negative { color: var(--red); }
    
    .vix-banner {
        background: rgba(251, 191, 36, 0.1);
        border: 1px solid var(--amber);
        color: var(--amber);
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 25px;
        text-align: center;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    /* Sections */
    .section-title {
        margin: 50px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--card-border);
        font-size: 1.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .opp-grid {
        display: grid;
        gap: 25px;
        margin-bottom: 40px;
    }
    
    .grid-top { grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); }
    .grid-watch { grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); }

    .opp-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 22px;
        position: relative;
    }
    
    .card-top { border: 1px solid var(--gold); }

    .opp-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 15px;
    }
    
    .opp-ticker { font-size: 1.7rem; font-weight: 800; margin: 0; color: var(--gold); }
    .opp-company { font-size: 0.85rem; color: var(--text-dim); display: block; }
    .opp-price { font-size: 1.3rem; font-weight: 600; }
    
    .badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-right: 8px;
    }
    .badge-swing { background: rgba(201, 163, 92, 0.15); color: var(--gold); }
    .badge-rise { background: rgba(74, 222, 128, 0.15); color: var(--green); }
    .badge-default { background: rgba(132, 141, 151, 0.15); color: var(--text-dim); }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin: 15px 0;
    }
    
    .metric-item { text-align: left; }
    .metric-label { font-size: 0.65rem; color: var(--text-dim); display: block; }
    .metric-val { font-size: 0.9rem; font-weight: 600; }
    
    .ai-report {
        background: rgba(201, 163, 92, 0.05);
        border-left: 3px solid var(--gold);
        padding: 12px;
        margin: 15px 0;
        font-size: 0.8rem;
        white-space: pre-wrap;
    }
    
    .ai-details summary {
        cursor: pointer;
        color: var(--gold-light);
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .link-buttons { display: flex; gap: 8px; margin-top: 15px; }
    .btn {
        flex: 1;
        text-align: center;
        padding: 6px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 600;
        text-decoration: none;
        background: #232a35;
        color: var(--text);
        border: 1px solid #30363d;
    }
    .btn:hover { background: #30363d; }
    
    /* Horizontal Flags */
    .flag-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 0.9rem;
    }
    .flag-sym { font-weight: 800; color: var(--gold); width: 80px; }
    .flag-name { color: var(--text-dim); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-right: 20px; }
    .flag-phase { width: 100px; font-weight: 600; }
    .flag-motive { color: var(--amber); font-weight: 600; flex: 1; text-align: right; margin-right: 20px; }
    .flag-upside { width: 80px; text-align: right; font-weight: 700; color: var(--green); }

    /* Skip Today */
    .skip-details {
        background: #111418;
        border: 1px solid #232a35;
        padding: 5px 15px;
        border-radius: 6px;
        margin-bottom: 6px;
    }
    .skip-details summary {
        cursor: pointer;
        padding: 8px 0;
        font-size: 0.85rem;
        color: var(--text-dim);
    }
    .skip-content {
        padding-bottom: 10px;
        font-size: 0.8rem;
        color: var(--red);
        font-weight: 600;
    }

    footer {
        text-align: center;
        margin-top: 60px;
        padding: 30px 0;
        border-top: 1px solid var(--card-border);
        color: var(--text-dim);
        font-size: 0.75rem;
    }
    </style>
    """
    
    # 4. BUILD HTML COMPONENTS
    
    # Macro section
    macro_html = ""
    if macro_data:
        if macro_data.get('alerta_vix'):
            macro_html += f'<div class="vix-banner">⚠️ VIX ALERT: {macro_data.get("VIX", {}).get("value", "N/A")} — High Volatility. Strategy: Defensive.</div>'
        
        macro_html += '<div class="macro-grid">'
        for key in ["SPY", "QQQ", "VIX", "TNX", "DXY"]:
            item = macro_data.get(key, {})
            val = item.get('value', 'N/A')
            change = item.get('change_pct', 0)
            change_cls = "positive" if change >= 0 else "negative"
            prefix = "+" if change >= 0 else ""
            macro_html += f"""
            <div class="macro-tile">
                <span class="macro-label">{item.get('name', key)}</span>
                <span class="macro-value">{val if isinstance(val, str) else f"{val:.2f}"}</span>
                <span class="macro-change {change_cls}">{prefix}{change:.2f}%</span>
            </div>
            """
        macro_html += '</div>'
    else:
        macro_html = '<div style="text-align:center; color:var(--text-dim); margin-bottom:30px;">Market data unavailable.</div>'

    # Summary Bar
    summary_bar_html = f"""
    <div class="summary-bar">
        <span>⭐ {n_top} Top Picks</span>
        <span>📋 {n_watch} On Watch</span>
        <span>⚠️ {n_flags} With Flags</span>
        <span>❌ {n_skip} Skip Today</span>
    </div>
    """

    # SECTIONS RENDERER
    sections_html = ""
    
    # helper for card info
    def get_card_body(op, mode="full"):
        m = getattr(op, "metrics", {}) or (op.get("metrics", {}) if isinstance(op, dict) else {})
        bucket = m.get("bucket", "UNKNOWN")
        subtype = m.get("subtype", "")
        badge_cls = f"badge-{bucket.lower()}" if bucket.lower() in ["swing", "rise"] else "badge-default"
        phase = m.get("phase", "N/A")
        pe_map = {"VALLEY":"🟢","MID":"🟡","MATURE":"🟠","LATE":"🔴"}
        pe = pe_map.get(phase, "⚪")
        
        report_text = (reports or {}).get(op.symbol) or getattr(op, "explanation", "")
        if mode == "full":
            ai_html = f'<div class="ai-report">{report_text}</div>' if report_text else '<div style="margin:15px 0; color:var(--text-dim); font-size:0.8rem; font-style:italic;">No AI report available.</div>'
        else: # collapsed
            ai_html = f'<details class="ai-details"><summary>View AI Analysis</summary><div class="ai-report">{report_text}</div></details>' if report_text else ''

        return f"""
            <div class="opp-header">
                <div>
                    <h2 class="opp-ticker">{op.symbol}</h2>
                    <span class="opp-company">{op.company_name or ""}</span>
                </div>
                <div class="opp-price">${op.current_price:.2f}</div>
            </div>
            <div>
                <span class="badge {badge_cls}">{bucket} {'→ ' + subtype if subtype else ''}</span>
                <span style="font-size:0.85rem;">{pe} {phase}</span>
            </div>
            <div class="metrics-grid">
                <div class="metric-item"><span class="metric-label">Drop %</span><span class="metric-val">{m.get('drop_from_high_pct', 0):.1f}%</span></div>
                <div class="metric-item"><span class="metric-label">Rebound %</span><span class="metric-val">{m.get('rebound_pct', 0):.1f}%</span></div>
                <div class="metric-item"><span class="metric-label">RSI(14)</span><span class="metric-val">{m.get('rsi_14', 'N/A')}</span></div>
                <div class="metric-item"><span class="metric-label">Vol 3M</span><span class="metric-val">{m.get('vol_ratio_3m', 1):.1f}x</span></div>
                <div class="metric-item"><span class="metric-label">Upside 3Y</span><span class="metric-val">{m.get('upside_to_ath3y', 0):.1f}%</span></div>
                <div class="metric-item"><span class="metric-label">Progress</span><span class="metric-val">{m.get('progress_pct', 0):.0f}%</span></div>
            </div>
            {ai_html}
            <div class="link-buttons">
                <a href="https://finance.yahoo.com/quote/{op.symbol}" class="btn" target="_blank">Yahoo</a>
                <a href="https://finviz.com/quote.ashx?t={op.symbol}" class="btn" target="_blank">Finviz</a>
                <a href="https://www.sec.gov/cgi-bin/browse-edgar?CIK={op.symbol}" class="btn" target="_blank">SEC</a>
            </div>
        """

    # SECTION A: Top Picks
    if categories["top_pick"]:
        sections_html += '<h2 class="section-title">⭐ Top Picks</h2>'
        sections_html += '<div class="opp-grid grid-top">'
        for op in categories["top_pick"]:
            sections_html += f'<div class="opp-card card-top">{get_card_body(op, "full")}</div>'
        sections_html += '</div>'

    # SECTION B: On Watch
    if categories["on_watch"]:
        sections_html += '<h2 class="section-title">📋 On Watch</h2>'
        sections_html += '<div class="opp-grid grid-watch">'
        for op in categories["on_watch"]:
            sections_html += f'<div class="opp-card">{get_card_body(op, "collapsed")}</div>'
        sections_html += '</div>'

    # DIVIDER
    if (categories["top_pick"] or categories["on_watch"]) and (categories["with_flags"] or categories["skip_today"]):
        sections_html += '<hr style="border: 0; border-top: 1px solid #30363d; margin: 40px 0;">'

    # SECTION C: With Flags
    if categories["with_flags"]:
        sections_html += '<h2 class="section-title">⚠️ Detected with Flags</h2>'
        for op in categories["with_flags"]:
            m = getattr(op, "metrics", {}) or (op.get("metrics", {}) if isinstance(op, dict) else {})
            motive = get_flag_motive(op)
            upside = m.get('upside_to_ath3y', 0)
            sections_html += f"""
            <div class="flag-row">
                <span class="flag-sym">{op.symbol}</span>
                <span class="flag-name">{op.company_name or ""}</span>
                <span class="flag-phase">{m.get('phase', '')}</span>
                <span class="flag-motive">{motive}</span>
                <span class="flag-upside">+{upside:.1f}%</span>
            </div>
            """

    # SECTION D: Skip Today
    if categories["skip_today"]:
        sections_html += '<h2 class="section-title">❌ Skip Today</h2>'
        for op in categories["skip_today"]:
            reason = get_skip_reason(op)
            sections_html += f"""
            <details class="skip-details">
                <summary>{op.symbol} — {op.company_name or ""}</summary>
                <div class="skip-content">REASON: {reason}</div>
            </details>
            """

    # FINAL ASSEMBLY
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RadarCore | {timestamp}</title>
        {css}
    </head>
    <body>
        <div class="container">
            <header>
                <h1><span class="pulse-dot"></span>RadarCore Intelligence</h1>
                <div class="timestamp">Market Scan Analysis · {timestamp}</div>
            </header>
            
            {macro_html}
            {summary_bar_html}
            {sections_html}
            
            <footer>
                <p>RadarCore Engine v2.5 · {timestamp}</p>
                <p style="opacity:0.5; max-width:600px; margin:10px auto;">
                    This report is generated automatically based on technical and fundamental data. 
                    Not financial advice. High risk investment detected.
                </p>
            </footer>
        </div>
    </body>
    </html>
    """
    return html
