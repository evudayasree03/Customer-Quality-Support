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
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500&family=IBM+Plex+Sans:wght@300;400;500&family=Sora:wght@300;400;500;600&family=Bebas+Neue&display=swap');

:root {
  /* Color Palette - SarvInfo Inspired */
  --bg-base:    #FDFCF7;        /* Clean Off-white */
  --bg-surface: #FFFFFF;        /* Pure White */
  --bg-overlay: rgba(255,255,255,0.85);
  --accent:     #EB643E;        /* Vibrant Sarv Orange */
  --accent-dim: rgba(235,100,62,0.08);
  --accent-glow:rgba(235,100,62,0.25);
  --secondary:  #749CE2;        /* Soft Blue Accent */
  
  /* Semantic Colors */
  --text-primary:   #212529;    /* Deep Charcoal */
  --text-secondary: #64748B;    /* Muted Slate */
  --text-muted:     #94A3B8;
  --danger:     #EF4444;
  --warn:       #F59E0B;
  --ok:         #10B981;
  --border:     rgba(0,0,0,0.06);
  --border-m:   rgba(235,100,62,0.2);

  /* Geometry & FX */
  --radius:     16px;           /* Softer, more modern corners */
  --radius-sm:  10px;
  --blur:       12px;
  --shadow:     0 4px 12px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.02);
  
  /* Typography */
  --font-mono:  'IBM Plex Mono', monospace;
  --font-sans:  'Sora', 'IBM Plex Sans', sans-serif;
  --font-display: 'Bebas Neue', sans-serif;
}

/* App-Wide Reset */
.stApp, html, body, [class*="css"] {
  background-color: var(--bg-base) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-sans) !important;
}
.stApp {
  background: var(--bg-base) !important;
}

/* Sidebar & Navigation */
section[data-testid="stSidebar"] {
  background: var(--bg-surface) !important;
  border-right: 1px solid var(--border) !important;
  box-shadow: 2px 0 10px rgba(0,0,0,0.02) !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
  font-size: 0.9rem !important;
  color: var(--text-secondary) !important;
}

/* Metrics & KPI Visualization */
div[data-testid="metric-container"] {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 1.2rem 1.4rem !important;
  box-shadow: var(--shadow) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
div[data-testid="metric-container"]:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.06) !important;
  border-color: var(--accent-glow) !important;
}
div[data-testid="metric-container"] label {
  color: var(--text-secondary) !important;
  font-family: var(--font-sans) !important;
  font-weight: 500 !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.05em !important;
  text-transform: uppercase !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
  color: var(--accent) !important;
  font-family: var(--font-display) !important;
  font-size: 2.2rem !important;
  letter-spacing: 0.02em !important;
}

/* Buttons & Calls to Action */
.stButton > button {
  background: linear-gradient(135deg, #EB643E 0%, #F1683E 100%) !important;
  color: #FFFFFF !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  font-family: var(--font-sans) !important;
  font-size: 0.85rem !important;
  letter-spacing: 0.02em !important;
  font-weight: 600 !important;
  padding: 0.6rem 1.6rem !important;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: 0 4px 12px var(--accent-glow) !important;
}
.stButton > button:hover {
  box-shadow: 0 6px 20px var(--accent-glow) !important;
  transform: translateY(-1px) !important;
  opacity: 0.95 !important;
}

/* Secondary Actions / Outlined Buttons */
.stButton > button[kind="secondary"] {
  background: transparent !important;
  color: var(--accent) !important;
  border: 1.5px solid var(--accent) !important;
  box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
  background: var(--accent-dim) !important;
  box-shadow: none !important;
}

/* Modern Clean Containers */
.glass-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow);
}

/* Audit Specific Styles */
.violation-flag {
  background: rgba(239,68,68,0.05);
  border-left: 4px solid var(--danger);
  padding: 10px 14px;
  border-radius: 4px;
  margin: 6px 0;
  font-size: 0.8rem;
  color: #991B1B;
}
.ok-flag {
  background: rgba(16,185,129,0.05);
  border-left: 4px solid var(--ok);
  padding: 10px 14px;
  border-radius: 4px;
  margin: 6px 0;
  font-size: 0.8rem;
  color: #065F46;
}

.section-header {
  font-family: var(--font-display);
  font-size: 1.6rem;
  color: var(--text-primary);
  letter-spacing: 0.02em;
  margin-bottom: 0.8rem;
  border-bottom: 2px solid var(--accent);
  display: inline-block;
  padding-right: 2rem;
}

.mono-badge {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  padding: 3px 10px;
  background: var(--bg-surface);
  border: 1px solid var(--border-m);
  border-radius: 20px;
  color: var(--accent);
  display: inline-block;
}

/* Transcript Enhancements */
.stChatFloatingInputContainer {
  background-color: var(--bg-base) !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: var(--bg-base);
}
::-webkit-scrollbar-thumb {
  background: var(--border-m);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--accent);
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
