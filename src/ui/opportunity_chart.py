import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta

def render_opportunity_chart(symbol: str, hist_data: pd.DataFrame, metrics: dict) -> None:
    """
    Renders a high-fidelity Plotly chart for a swing trading opportunity.
    """
    if hist_data.empty or not metrics:
        st.error(f"No data available to render chart for {symbol}")
        return

    # Extract metrics for easier access
    p_high = metrics.get("period_high")
    p_low = metrics.get("period_low")
    drop = metrics.get("drop_from_high_pct", metrics.get("drop_pct", 0))
    rebound = metrics.get("rebound_pct", 0)
    p_type = metrics.get("pattern_type", "N/A")
    conf = metrics.get("confidence", 0)
    
    # Header: Summary Metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"**{symbol}** | `{p_type}` | **{conf}%** Conf.")
    with c2:
        st.markdown(f"Drop: <span style='color:#e74c3c'>{drop:.1f}%</span> | Rebound: <span style='color:#2ecc71'>{rebound:.1f}%</span>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"Stop: `${p_low:.2f}` | Target: `${p_high:.2f}`")

    # Find dates for period_high and period_low in the data
    # We find the first occurrence to be consistent with the logic
    try:
        # We need to find the specific rows matching these precise prices
        # Since these come from 'High' and 'Low', we look for them there
        high_date = hist_data[hist_data['High'] == p_high].index[0]
        low_date = hist_data[hist_data['Low'] == p_low].index[0]
        now_date = hist_data.index[-1]
    except Exception:
        # Fallback if exact price match fails due to rounding
        st.warning("⚠️ Precise dates for highlights could not be determined. Showing raw price only.")
        fig = go.Figure(data=[go.Scatter(x=hist_data.index, y=hist_data['Close'], line=dict(color='#bdc3c7', width=2))])
        fig.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)
        return

    # Create Figure
    fig = go.Figure()

    # 1. Price Line (Close)
    fig.add_trace(go.Scatter(
        x=hist_data.index, 
        y=hist_data['Close'],
        name='Close Price',
        line=dict(color='#ecf0f1', width=2),
        fill='tozeroy',
        fillcolor='rgba(189, 195, 199, 0.05)'
    ))

    # 2. Zones (vrect)
    # Red Zone: High to Low (The Drop)
    fig.add_vrect(
        x0=high_date, x1=low_date,
        fillcolor="rgba(231, 76, 60, 0.15)",
        layer="below", line_width=0,
        annotation_text="DEVALUATION", annotation_position="top left",
        annotation_font_size=10, annotation_font_color="rgba(231, 76, 60, 0.5)"
    )
    
    # Green Zone: Low to Now (The Recovery)
    fig.add_vrect(
        x0=low_date, x1=now_date,
        fillcolor="rgba(46, 204, 113, 0.15)",
        layer="below", line_width=0,
        annotation_text="RECOVERY", annotation_position="top left",
        annotation_font_size=10, annotation_font_color="rgba(46, 204, 113, 0.5)"
    )

    # 3. Reference Lines
    # Stop Loss (Low)
    fig.add_hline(y=p_low, line_dash="dash", line_color="#e74c3c", annotation_text="Stop / Low")
    # Target 1 (85% of high - approximation of pivot/resistance)
    t1_val = p_high * 0.85 
    fig.add_hline(y=t1_val, line_dash="dash", line_color="#f1c40f", annotation_text="T1 Resistance")
    # Target 2 (Previous High)
    fig.add_hline(y=p_high, line_dash="dash", line_color="#2ecc71", annotation_text="T2 Target")

    # 4. Markers
    # Triangle Down at Period High
    fig.add_trace(go.Scatter(
        x=[high_date], y=[p_high],
        mode='markers+text',
        name='High Peak',
        text=["START"], textposition="top center",
        marker=dict(symbol='triangle-down', size=15, color='#e74c3c')
    ))
    
    # Triangle Up at Period Low
    fig.add_trace(go.Scatter(
        x=[low_date], y=[p_low],
        mode='markers+text',
        name='Local Bottom',
        text=["PIVOT"], textposition="bottom center",
        marker=dict(symbol='triangle-up', size=15, color='#f1c40f')
    ))

    # Special logic for Patterns
    if p_type == "L-BASE":
        # Orange block for last 15 days
        base_start = now_date - timedelta(days=15)
        fig.add_vrect(
            x0=base_start, x1=now_date,
            fillcolor="rgba(230, 126, 34, 0.2)",
            layer="below", line_width=1, line_color="rgba(230, 126, 34, 0.5)",
            annotation_text="ACCUMULATION BASE", annotation_position="bottom right"
        )
    elif p_type == "V-RECOVERY":
        # Green Breakout dot at latest date
        fig.add_trace(go.Scatter(
            x=[now_date], y=[hist_data['Close'].iloc[-1]],
            mode='markers+text',
            name='Breakout',
            text=["BREAKOUT"], textposition="top right",
            marker=dict(symbol='star', size=12, color='#2ecc71')
        ))

    # Layout Styling
    # Frame time: 20 days before high to now
    start_view = high_date - timedelta(days=20)
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f0f0f",
        plot_bgcolor="#0f0f0f",
        height=400,
        margin=dict(l=20, r=20, t=10, b=20),
        showlegend=False,
        xaxis=dict(
            range=[start_view, now_date],
            gridcolor="#2c3e50"
        ),
        yaxis=dict(
            gridcolor="#2c3e50",
            side="right"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
