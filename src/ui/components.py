"""
SamiX UI Component Library

This module contains reusable Streamlit components for data visualization
and session reporting. It includes:
- ECharts Gauges: For high-impact metric visualization.
- Plotly Charts: For detailed turn-by-turn sentiment and quality analysis.
- Specialized Renderers: For speaker-separated transcripts and RAG-verified 'wrong turns'.
"""
from __future__ import annotations

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Optional

from src.utils.history_manager import (
    AuditScores, TranscriptTurn, WrongTurn
)


# ECharts Gauges 

def render_gauge(value: float, title: str, max_val: float = 10.0) -> None:
    """
    Renders a sophisticated half-ring ECharts gauge.
    Automatically applies semantic coloring (Green/Amber/Red) based on the score.
    """
    try:
        from streamlit_echarts import st_echarts
    except ImportError:
        # Fallback to standard Streamlit metrics if the ECharts component is missing.
        st.metric(title, f"{value:.1f}/{max_val:.0f}")
        st.progress(value / max_val)
        return

    # Normalize value to a percentage for the gauge progress bar.
    pct     = min(100.0, max(0.0, value / max_val * 100))
    colour  = "#10B981" if pct >= 70 else "#F59E0B" if pct >= 50 else "#EF4444"

    option = {
        "backgroundColor": "transparent",
        "series": [{
            "type": "gauge",
            "startAngle": 200, "endAngle": -20,
            "min": 0, "max": 100,
            "splitNumber": 5,
            "itemStyle": {"color": colour, "shadowColor": colour, "shadowBlur": 8},
            "progress": {"show": True, "width": 14},
            "pointer":  {"show": False},
            "axisLine": {
                "lineStyle": {"width": 14, "color": [[1, "rgba(255,255,255,0.06)"]]}
            },
            "axisTick":  {"show": False},
            "splitLine": {"show": False},
            "axisLabel": {"show": False},
            "title": {
                "show": True,
                "offsetCenter": [0, "75%"],
                "fontSize": 11,
                "color": "#94A3B8",
                "fontFamily": "IBM Plex Mono",
            },
            "detail": {
                "show": True,
                "offsetCenter": [0, "15%"],
                "formatter": f"{value:.1f}",
                "fontSize": 30,
                "fontWeight": "bold",
                "color": colour,
                "fontFamily": "IBM Plex Mono",
            },
            "data": [{"value": pct, "name": title.upper()}],
        }]
    }
    st_echarts(options=option, height="170px", key=f"gauge_{title}_{id(value)}")


def render_three_gauges(scores: AuditScores) -> None:
    """ Renders the top 3 quality dimensions side-by-side. """
    c1, c2, c3 = st.columns(3)
    with c1:
        render_gauge(scores.empathy,        "Empathy")
    with c2:
        render_gauge(scores.professionalism, "Professionalism")
    with c3:
        render_gauge(scores.compliance,      "Compliance")


# Dual Score Chart 

def render_dual_score_chart(scores: AuditScores) -> None:
    """
    Renders a Plotly line chart comparing Agent Quality vs. Customer Sentiment.
    Highlights 'danger zones' (scores < 40%) with red background shading.
    """
    n_agent = len(scores.agent_by_turn)
    n_cust  = len(scores.customer_sentiment)
    n       = max(n_agent, n_cust, 1)

    # Pad data to ensure both lines have the same length.
    agent_data = scores.agent_by_turn + [5.0] * (n - n_agent)
    cust_data  = scores.customer_sentiment + [5.0] * (n - n_cust)
    x_labels   = [f"T{i+1}" for i in range(n)]

    fig = go.Figure()

    # Highlight turns where performance or sentiment dipped below the failure threshold.
    for i, (a, c) in enumerate(zip(agent_data, cust_data)):
        if a < 4.0 or c < 4.0:
            fig.add_vrect(
                x0=i - 0.4, x1=i + 0.4,
                fillcolor="rgba(239,68,68,0.12)",
                layer="below", line_width=0,
            )

    # Primary Line: Agent Quality
    fig.add_trace(go.Scatter(
        x=x_labels, y=agent_data,
        mode="lines+markers",
        name="Agent quality",
        line=dict(color="#8B5CF6", width=2.5),
        marker=dict(
            size=7,
            color=["#EF4444" if v < 4 else "#F59E0B" if v < 7 else "#10B981" for v in agent_data],
            line=dict(width=1, color="#0F172A"),
        ),
        hovertemplate="<b>%{x}</b><br>Agent: %{y:.1f}/10<extra></extra>",
    ))

    # Secondary Line: Customer Sentiment (Dashed)
    fig.add_trace(go.Scatter(
        x=x_labels, y=cust_data,
        mode="lines+markers",
        name="Customer sentiment",
        line=dict(color="#6EE7B7", width=2, dash="dot"),
        marker=dict(
            size=5,
            color=["#EF4444" if v < 4 else "#F59E0B" if v < 7 else "#6EE7B7" for v in cust_data],
        ),
        hovertemplate="<b>%{x}</b><br>Sentiment: %{y:.1f}/10<extra></extra>",
    ))

    # Static fail threshold marker.
    fig.add_hline(y=4.0, line_dash="dash", line_color="rgba(239,68,68,0.4)",
                  annotation_text="40% threshold", annotation_font_size=9,
                  annotation_font_color="#EF4444")

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.6)",
        font=dict(family="IBM Plex Mono", color="#94A3B8", size=10),
        legend=dict(
            bgcolor="rgba(30,41,59,0.7)",
            bordercolor="rgba(139,92,246,0.2)",
            font=dict(size=10),
        ),
        xaxis=dict(
            gridcolor="rgba(139,92,246,0.1)",
            zerolinecolor="rgba(0,0,0,0)",
        ),
        yaxis=dict(
            range=[0, 10.5],
            dtick=2,
            gridcolor="rgba(139,92,246,0.1)",
            zerolinecolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        height=280,
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)


# Transcript Renderer 

def render_transcript(
    turns: list[TranscriptTurn],
    wrong_turns: Optional[list[WrongTurn]] = None,
) -> None:
    """
    Renders a color-coded chat interface.
    Agent and Customer turns are visually distinct. Critical 'wrong turns'
    are flagged with warning banners directly beneath the offending turn.
    """
    wrong_map: dict[int, WrongTurn] = {}
    if wrong_turns:
        for wt in wrong_turns:
            wrong_map[wt.turn_number] = wt

    for turn in turns:
        spk_colour = "#8B5CF6" if turn.speaker == "AGENT" else "#64748B"
        bg_alpha   = "0.1"    if turn.speaker == "AGENT" else "0.05"

        col_spk, col_text = st.columns([1, 5])
        with col_spk:
            st.markdown(
                f'<div style="text-align:right;padding-top:10px;">'
                f'<span style="font-family:IBM Plex Mono;font-size:0.68rem;'
                f'color:{spk_colour};letter-spacing:0.08em;font-weight:500;">'
                f'{turn.speaker}</span><br>'
                f'<span style="font-size:0.62rem;color:#475569;">{turn.timestamp}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col_text:
            st.markdown(
                f'<div style="background:rgba(139,92,246,{bg_alpha});'
                f'border-left:2px solid {spk_colour};'
                f'padding:8px 12px;border-radius:0 6px 6px 0;'
                f'margin-bottom:3px;font-size:0.82rem;color:#E2E8F0;">'
                f'{turn.text}'
                f'</div>',
                unsafe_allow_html=True,
            )

        # If this turn was flagged as a violation, render the audit warning.
        if turn.turn in wrong_map:
            wt = wrong_map[turn.turn]
            st.markdown(
                f'<div class="violation-flag">'
                f'⚠ T{wt.turn_number} · {wt.score_impact} · '
                f'{wt.what_went_wrong[:120]}…<br>'
                f'<span style="opacity:.7;font-size:0.7rem;">RAG: {wt.rag_source}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )


# Fact-Verification UI 

def render_wrong_turns(
    wrong_turns: list[WrongTurn],
    specific_corrections: Optional[dict[int, str]] = None,
) -> None:
    """
    Deep-dive view for factual and policy errors.
    Shows the offending quote, the RAG-verified fact, and a correction field.
    """
    if not wrong_turns:
        st.success("✓ No critical failures detected in this session.")
        return

    for wt in wrong_turns:
        with st.expander(
            f"🔴 Turn {wt.turn_number} — {wt.speaker}  ·  {wt.score_impact}",
            expanded=True,
        ):
            st.markdown("**What was said:**")
            st.markdown(
                f'<div style="font-style:italic;background:rgba(30,41,59,0.8);'
                f'border-left:3px solid #475569;padding:8px 12px;border-radius:0 6px 6px 0;'
                f'color:#94A3B8;font-size:0.85rem;">'
                f'"{wt.agent_said}"'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.markdown("")

            st.markdown("**What went wrong:**")
            st.markdown(
                f'<div class="violation-flag">{wt.what_went_wrong}</div>',
                unsafe_allow_html=True,
            )

            st.markdown("**Correct fact (RAG verified):**")
            st.markdown(
                f'<div class="ok-flag">'
                f'{wt.correct_fact}<br>'
                f'<span style="opacity:0.6;font-size:0.7rem;">'
                f'Source: {wt.rag_source} · conf {wt.rag_confidence:.2f}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.markdown("**Specific correction the agent should have used:**")
            key = f"correction_{wt.turn_number}"
            default = specific_corrections.get(wt.turn_number, wt.specific_correction) \
                if specific_corrections else wt.specific_correction
            st.text_area(
                label="Edit and save to session feedback",
                value=default,
                height=90,
                key=key,
                label_visibility="collapsed",
            )


# Financial Reporting 

def render_cost_card(
    token_count: int,
    cost_usd: float,
    revenue_per_call: float = 5.0,
) -> None:
    """ Renders a metric row summarizing API costs vs. revenue profit. """
    profit = revenue_per_call - cost_usd
    margin = (profit / revenue_per_call * 100) if revenue_per_call else 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tokens used",       f"{token_count:,}")
    c2.metric("API cost",          f"${cost_usd:.5f}")
    c3.metric("Revenue / audit",   f"${revenue_per_call:.2f}")
    c4.metric(
        "Profit / audit",
        f"${profit:.4f}",
        delta=f"{margin:.1f}% margin",
        delta_color="normal",
    )


# Metadata Components 

def render_filename_badge(uploaded_name: str, stored_name: str) -> None:
    """ Displays a badge verifying that the stored filename matches the upload. """
    match = uploaded_name == stored_name
    icon  = "✓" if match else "✗"
    colour = "rgba(16,185,129,0.8)" if match else "rgba(239,68,68,0.8)"
    st.markdown(
        f'<div style="font-family:IBM Plex Mono;font-size:0.72rem;'
        f'color:{colour};padding:4px 0;">'
        f'{icon} Stored as: <code style="color:{colour}">{stored_name}</code>'
        f'&nbsp;&nbsp;(matches uploaded filename)</div>',
        unsafe_allow_html=True,
    )


def build_history_dataframe(sessions: list) -> pd.DataFrame:
    """ Converts a list of AuditSession objects into a Pandas DataFrame for UI display. """
    rows = []
    for s in sessions:
        verdict_emoji = (
            "🟢" if s.scores.final_score >= 80 else
            "🟡" if s.scores.final_score >= 60 else "🔴"
        )
        rows.append({
            "Uploaded filename":     s.filename,
            "Stored history name":   s.stored_name,
            "Date / time":           s.upload_time,
            "Mode":                  s.mode.capitalize(),
            "Agent score":           f"{s.scores.final_score:.0f}/100",
            "Cust sentiment":        f"{s.scores.customer_overall:.1f}/10",
            "Verdict":               f"{verdict_emoji} {s.scores.verdict}",
            "Violations":            s.violations,
            "session_id":            s.session_id,
        })
    df = pd.DataFrame(rows)
    return df
