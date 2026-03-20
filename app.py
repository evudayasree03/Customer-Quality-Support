"""
SamiX - Quality Auditor Entry Point

This is the main driver for the SamiX application. It initializes the system components,
handles user authentication, and renders the appropriate UI (Agent or Admin) based on 
user roles.

Usage:
    streamlit run app.py
"""
from __future__ import annotations

import os

# Disable Hugging Face telemetry and legacy warnings for a cleaner console output.
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import streamlit as st

# Configure the primary page settings.
st.set_page_config(
    page_title="SamiX · Quality Auditor",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import our custom modules from the src directory.
from src.auth.authenticator   import AuthManager
from src.pipeline.alert_engine import AlertEngine
from src.pipeline.groq_client  import GroqClient
from src.pipeline.stt_processor import STTProcessor
from src.ui.admin_panel        import AdminPanel
from src.ui.agent_panel        import AgentPanel
from src.ui.login_page         import LoginPage
from src.ui.styles             import inject_css
from src.utils.audio_processor import AudioProcessor
from src.utils.cost_tracker    import CostTracker
from src.utils.history_manager import HistoryManager
from src.utils.kb_manager      import KBManager

# Apply custom CSS styles to match the premium dark-themed design.
inject_css()


@st.cache_resource
def _init():
    """ Initialize and cache singleton instances of core system managers. """
    return {
        "history": HistoryManager(),
        "groq":    GroqClient(),
        "stt":     STTProcessor(),
        "audio":   AudioProcessor(),
        "cost":    CostTracker(),
        "alerts":  AlertEngine(),
        "kb":      KBManager(),
    }


# Global Resource container and Authentication manager.
R    = _init()
auth = AuthManager()
R["auth"] = auth


def _sidebar_brand() -> None:
    """ Renders the SamiX branding and system status indicators in the sidebar. """
    with st.sidebar:
        # Logo placeholder
        st.markdown(
            '<div style="width:80px;height:80px;border:2px dashed rgba(139,92,246,.35);'
            'border-radius:12px;display:flex;align-items:center;justify-content:center;'
            'background:rgba(139,92,246,.06);margin:0 auto 1rem auto;">'
            '<span style="font-family:IBM Plex Mono;font-size:.65rem;'
            'color:rgba(139,92,246,.5);letter-spacing:.08em;">LOGO</span></div>',
            unsafe_allow_html=True,
        )
        # Main Title (SamiX)
        st.markdown(
            '<div style="text-align:center;">'
            '<div style="font-family:Bebas Neue,sans-serif;font-size:2rem;'
            'color:#E2E8F0;letter-spacing:.03em;line-height:1;">'
            'SAMI<span style="color:#8B5CF6;">X</span></div>'
            '<div style="font-family:IBM Plex Mono;font-size:.65rem;'
            'color:#8B5CF6;letter-spacing:.14em;margin-bottom:.3rem;">'
            'THE ALL-SEEING EYE OF QUALITY</div>'
            '<div style="font-family:IBM Plex Mono;font-size:.6rem;'
            'color:#334155;letter-spacing:.25em;">ಸಮೀಕ್ಷೆ</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()

        # Dynamic System Health Status
        statuses = [
            ("Groq API",    "LIVE"   if R["groq"].is_live         else "MOCK",    R["groq"].is_live),
            ("Deepgram",    "LIVE"   if R["stt"].has_deepgram      else "MOCK",    R["stt"].has_deepgram),
            ("Whisper",     "LOCAL", True),
            ("LangChain",   "READY", True),
            ("Milvus Lite", "VECTOR" if R["kb"].is_vector_enabled  else "KEYWORD", True),
            ("pydub",       "ACTIVE",True),
        ]
        st.markdown(
            '<div style="font-family:IBM Plex Mono;font-size:.68rem;'
            'color:#475569;letter-spacing:.1em;margin-bottom:.4rem;">SYSTEM STATUS</div>',
            unsafe_allow_html=True,
        )
        for svc, label, ok in statuses:
            colour = "#10B981" if ok else "#F59E0B"
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;'
                f'font-family:IBM Plex Mono;font-size:.68rem;padding:2px 0;">'
                f'<span style="color:#64748B;">{svc}</span>'
                f'<span style="color:{colour};">{label}</span></div>',
                unsafe_allow_html=True,
            )

        st.divider()
        # User account info and Logout
        st.markdown(
            f'<div style="font-family:IBM Plex Mono;font-size:.7rem;'
            f'color:#94A3B8;margin-bottom:.5rem;">'
            f'Signed in as<br>'
            f'<span style="color:#8B5CF6;">{auth.current_user_name}</span></div>',
            unsafe_allow_html=True,
        )
        auth.render_logout()


def _role() -> str:
    """ Sidebar toggle for switching between Agent and Admin views (if authorized). """
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        role = st.radio(
            "View as",
            ["Agent / Client", "Admin"],
            index=0, horizontal=True,
            label_visibility="collapsed",
        )
    return "admin" if role == "Admin" else "agent"


def main() -> None:
    """ Main application flow: Auth -> Sidebar -> Panel Routing. """
    # Enforce login first.
    if not auth.is_authenticated():
        LoginPage(auth).render()
        return

    # Render branding and common sidebar elements.
    _sidebar_brand()
    role = _role()

    # Route to the appropriate panel based on selected role.
    if role == "admin":
        AdminPanel(
            history=R["history"],
            kb=R["kb"],
            alerts=R["alerts"],
        ).render()
    else:
        AgentPanel(
            history=R["history"],
            groq=R["groq"],
            stt=R["stt"],
            audio=R["audio"],
            cost=R["cost"],
            alerts=R["alerts"],
            kb=R["kb"],
        ).render()


if __name__ == "__main__":
    main()
