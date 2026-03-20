"""
SamiX Login & Identity Gateway

This module implements a premium, dual-pane entry screen for the platform.
It features:
- Brand identity on the left with live (mock) KPI metrics.
- Secure authentication forms on the right for Sign In and Registration.
- Form-safe state management using Streamlit's native form containers.
"""
from __future__ import annotations

import streamlit as st

from src.auth.authenticator import AuthManager


class LoginPage:
    """
    Renders a high-fidelity login experience.
    
    The layout is split into a branding section and an interactive auth section
    to create a professional, enterprise-grade first impression.
    """

    def __init__(self, auth: AuthManager) -> None:
        """ Initializes the login page with the centralized AuthManager. """
        self._auth = auth

    def render(self) -> None:
        """
        Entry point for rendering the gateway.
        Uses a two-column responsive layout for balanced visual weight.
        """
        # Distribute branding and forms in a 1:1 ratio with large spacing.
        col_brand, col_form = st.columns([1, 1], gap="large")

        with col_brand:
            self._render_brand()

        with col_form:
            self._render_form()

    # Render Logic (Private) 

    def _render_brand(self) -> None:
        """
        Visual Branding Section.
        Displays the SamiX logo, tagline, and real-time operational metrics
        to build user confidence before sign-in.
        """
        st.markdown("<br><br>", unsafe_allow_html=True)

        # Logo Placeholder 
        # Designed as a distinct glassmorphic tile.
        st.markdown(
            '<div style="'
            'width:120px;height:120px;'
            'border:2px dashed rgba(139,92,246,0.4);'
            'border-radius:16px;'
            'display:flex;align-items:center;justify-content:center;'
            'background:rgba(139,92,246,0.06);'
            'margin-bottom:2rem;'
            '">'
            '<span style="font-size:0.7rem;font-family:IBM Plex Mono;'
            'color:rgba(139,92,246,0.6);letter-spacing:0.1em;">LOGO</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        # Title & Tagline 
        st.markdown(
            '<div style="font-family:Bebas Neue,sans-serif;font-size:3.2rem;'
            'color:#E2E8F0;line-height:0.9;letter-spacing:0.02em;margin-bottom:0.4rem;">'
            'SAMI<span style="color:#8B5CF6;">X</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-family:IBM Plex Mono;font-size:0.8rem;'
            'color:#8B5CF6;letter-spacing:0.18em;margin-bottom:1.2rem;">'
            'THE ALL-SEEING EYE OF QUALITY'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-family:IBM Plex Mono;font-size:0.72rem;'
            'color:#475569;line-height:2;">'
            'samiksha · ಸಮೀಕ್ಷೆ<br>'
            'GenAI-Powered Customer Support Auditor<br><br>'
            'Groq &nbsp;·&nbsp; Deepgram &nbsp;·&nbsp; Whisper<br>'
            'Milvus Lite &nbsp;·&nbsp; pydub &nbsp;·&nbsp; LangChain'
            '</div>',
            unsafe_allow_html=True,
        )

        # Live Operational Metrics 
        # Provide social proof and platform context.
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("Audits today",    "247")
        c2.metric("Avg QA score",    "73.4")
        c1.metric("Active agents",   "18")
        c2.metric("Violations",      "38")

    def _render_form(self) -> None:
        """
        Interactive Authentication Section.
        Toggles between Sign In and Registration workflows.
        """
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:Bebas Neue;font-size:1.8rem;'
            'color:#E2E8F0;letter-spacing:0.04em;margin-bottom:0.25rem;">'
            'Welcome</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-family:IBM Plex Mono;font-size:0.72rem;'
            'color:#475569;letter-spacing:0.12em;margin-bottom:1.5rem;">'
            'QUALITY AUDIT PLATFORM ACCESS'
            '</div>',
            unsafe_allow_html=True,
        )

        tab_login, tab_register = st.tabs(["Sign In", "Register"])

        with tab_login:
            # Wrap in form to allow 'Enter' key submission.
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Email Address", placeholder="name@company.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                
                submit = st.form_submit_button("Sign In →", use_container_width=True)

                if submit:
                    if not email or not password:
                        st.error("Please provide both email and password.", icon="⚠")
                    else:
                        success = self._auth.login(email, password)
                        if success:
                            st.rerun()
                        else:
                            st.error("Incorrect email or password.", icon="🔒")

            if self._auth.is_pending():
                st.info("Enter your credentials to securely access the quality audit platform.", icon="ℹ️")

        with tab_register:
            # Registration requires confirmation and field validation.
            with st.form("register_form", clear_on_submit=True):
                name = st.text_input("Full Name", placeholder="Jane Doe")
                email = st.text_input("Email Address", placeholder="name@company.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                confirm_pwd = st.text_input("Confirm Password", type="password", placeholder="••••••••")
                
                submit = st.form_submit_button("Register Account →", use_container_width=True)

                if submit:
                    if not name or not email or not password:
                        st.error("Please fill in all the fields.", icon="⚠")
                    elif password != confirm_pwd:
                        st.error("Passwords do not match.", icon="⚠")
                    else:
                        success = self._auth.register(email, name, password)
                        if success:
                            st.success(f"Account created for {email}! Please sign in from the 'Sign In' tab.", icon="✅")
                        else:
                            st.error("An account with this email already exists.", icon="⚠")
