"""
SamiX Global Style Engine

This module defines the visual identity of the SamiX platform. 
It uses a 'Deep Slate' and 'Electric Violet' color palette with 
glassmorphism effects and precise typography.

The styles are injected directly into the Streamlit DOM to override 
default behaviors and create a premium, enterprise-grade aesthetic.
"""

# Global CSS Definition 
# This multi-line string contains the entire design system, including 
# variables, core layout overrides, and specialized component classes.
CSS = """
<style>
/* Design System Tokens */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:wght@300;400;500&family=Bebas+Neue&display=swap');

:root {
  /* Color Palette */
  --bg-base:    #0F172A;        /* Deep Space Blue */
  --bg-surface: #1E293B;        /* Elevated Slate */
  --bg-overlay: rgba(30,41,59,0.75);
  --accent:     #8B5CF6;        /* Electric Violet */
  --accent-dim: rgba(139,92,246,0.18);
  --accent-glow:rgba(139,92,246,0.35);
  
  /* Semantic Colors */
  --text-primary:   #E2E8F0;
  --text-secondary: #94A3B8;
  --text-muted:     #475569;
  --danger:     rgba(239,68,68,0.8);
  --warn:       rgba(245,158,11,0.8);
  --ok:         rgba(16,185,129,0.8);

  /* Geometry & FX */
  --radius:     12px;
  --radius-sm:  8px;
  --blur:       16px;
  
  /* Typography */
  --font-mono:  'IBM Plex Mono', 'Courier New', monospace;
  --font-sans:  'IBM Plex Sans', system-ui, sans-serif;
  --font-display: 'Bebas Neue', sans-serif;
}

/* App-Wide Reset */
.stApp, html, body, [class*="css"] {
  background-color: var(--bg-base) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-mono) !important;
}
.stApp {
  background:
    radial-gradient(ellipse at 20% 10%, rgba(139,92,246,0.06) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 90%, rgba(59,130,246,0.04) 0%, transparent 50%),
    #0F172A !important;
}

/* Sidebar & Navigation */
section[data-testid="stSidebar"] {
  background: var(--bg-overlay) !important;
  backdrop-filter: blur(var(--blur)) !important;
  -webkit-backdrop-filter: blur(var(--blur)) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div {
  padding-top: 1rem !important;
}

/* Metrics & KPI Visualization */
div[data-testid="metric-container"] {
  background: var(--bg-overlay) !important;
  backdrop-filter: blur(var(--blur)) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 1rem 1.25rem !important;
  transition: border-color 0.2s;
}
div[data-testid="metric-container"]:hover {
  border-color: var(--border-m) !important;
}
div[data-testid="metric-container"] label {
  color: var(--text-secondary) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.7rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
  color: var(--accent) !important;
  font-family: var(--font-display) !important;
  font-size: 1.8rem !important;
}

/* Buttons & Calls to Action */
.stButton > button {
  background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
  color: #FFFFFF !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.06em !important;
  font-weight: 500 !important;
  padding: 0.55rem 1.4rem !important;
  transition: all 0.2s !important;
  box-shadow: 0 0 12px var(--accent-glow) !important;
}
.stButton > button:hover {
  box-shadow: 0 0 22px var(--accent-glow), 0 4px 16px rgba(0,0,0,0.4) !important;
  transform: translateY(-1px) !important;
}

/* Glassmorphic Containers */
.glass-card {
  background: var(--bg-overlay);
  backdrop-filter: blur(var(--blur));
  -webkit-backdrop-filter: blur(var(--blur));
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  margin-bottom: 0.75rem;
}

/* Audit Specific Styles */
.violation-flag {
  background: rgba(239,68,68,0.08);
  border-left: 3px solid rgba(239,68,68,0.6);
  padding: 8px 12px;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  margin: 4px 0;
  font-size: 0.78rem;
  color: rgba(252,165,165,0.9);
}
.ok-flag {
  background: rgba(16,185,129,0.08);
  border-left: 3px solid rgba(16,185,129,0.4);
  padding: 8px 12px;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  margin: 4px 0;
  font-size: 0.78rem;
  color: rgba(110,231,183,0.9);
}

.section-header {
  font-family: var(--font-display);
  font-size: 1.4rem;
  color: var(--accent);
  letter-spacing: 0.04em;
  margin-bottom: 0.5rem;
}

.mono-badge {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  padding: 2px 8px;
  border: 1px solid var(--border-m);
  border-radius: 4px;
  color: var(--text-secondary);
  display: inline-block;
}
</style>
"""


def inject_css() -> None:
    """
    Bootstrap function.
    Injects the custom CSS engine into the Streamlit session.
    Must be called early in the page render cycle.
    """
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)
