"""
SamiX Authentication Manager

This module provides a local, file-based authentication system using YAML for storage
and bcrypt for secure password hashing. It handles user login, registration, and
session state management for the Streamlit application.
"""
from __future__ import annotations

import streamlit as st
import os
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
import bcrypt

class AuthManager:
    """
    Manages user credentials and session authentication status.
    
    Credentials are stored in `data/auth/users.yaml`. The manager supports
    email-based usernames and secure password verification.
    """

    _USERS_YAML: str  = "data/auth/users.yaml"

    def __init__(self) -> None:
        """ Initialize the manager and load the user database. """
        self._load_config()

    def _load_config(self) -> None:
        """
        Loads the YAML configuration from disk.
        If the file doesn't exist, a default 'admin' account is created.
        """
        yaml_path = Path(self._USERS_YAML)
        
        if not yaml_path.exists():
            yaml_path.parent.mkdir(parents=True, exist_ok=True)
            # Default admin account info (Password: 'admin')
            default_config = {
                "credentials": {
                    "admin@samix.ai": {
                        "name": "Admin",
                        "password": "$2b$12$R.S/XfIay1V/2n3bF/O51uA3Vw0sSBYh4Cih.qInMFRc/VXZiJgGW" 
                    }
                }
            }
            with open(yaml_path, "w", encoding="utf-8") as file:
                yaml.dump(default_config, file, default_flow_style=False)

        # Parse the YAML file using a SafeLoader.
        with open(yaml_path, "r", encoding="utf-8") as file:
            self._config = yaml.load(file, Loader=SafeLoader)
            if "credentials" not in self._config:
                self._config["credentials"] = {}

    def save_config(self) -> None:
        """ Persists the current in-memory user database back to the YAML file. """
        with open(self._USERS_YAML, "w", encoding="utf-8") as file:
            yaml.dump(self._config, file, default_flow_style=False)

    def login(self, email: str, password: str) -> bool:
        """
        Verifies user credentials.
        Updates Streamlit session state on successful authentication.
        """
        email = email.lower().strip()
        creds = self._config.get("credentials", {})
        
        if email in creds:
            user = creds[email]
            hashed_pw = user.get("password", "")
            # Securely compare the provided password with the stored hash.
            if self._check_password(password, hashed_pw):
                st.session_state["authentication_status"] = True
                st.session_state["name"] = user.get("name", "User")
                st.session_state["email"] = email
                return True
                
        st.session_state["authentication_status"] = False
        return False

    def register(self, email: str, name: str, password: str) -> bool:
        """
        Registers a new user with a hashed password.
        Returns False if the email is already in use.
        """
        email = email.lower().strip()
        creds = self._config.setdefault("credentials", {})
        
        if email in creds:
            return False # Prevent duplicate registration.
            
        hashed_pw = self._hash_password(password)
        creds[email] = {
            "name": name,
            "password": hashed_pw
        }
        self.save_config()
        return True

    def _hash_password(self, raw: str) -> str:
        """ Generates a secure bcrypt hash for a raw password string. """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(raw.encode('utf-8'), salt).decode('utf-8')

    def _check_password(self, raw: str, hashed: str) -> bool:
        """ Validates a raw password against a bcrypt hash. """
        try:
            return bcrypt.checkpw(raw.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False

    def is_authenticated(self) -> bool:
        """ Returns True if the current session is successfully authenticated. """
        return st.session_state.get("authentication_status") is True

    def is_failed(self) -> bool:
        """ Returns True if the last login attempt failed. """
        return st.session_state.get("authentication_status") is False

    def is_pending(self) -> bool:
        """ Returns True if no authentication attempt has been made yet. """
        return st.session_state.get("authentication_status") is None

    def render_logout(self) -> None:
        """ Clears session state and triggers a page refresh to log the user out. """
        if st.sidebar.button("Sign Out", key="sidebar_logout_btn"):
            st.session_state["authentication_status"] = None
            st.session_state["name"] = None
            st.session_state["email"] = None
            st.rerun()

    @property
    def current_user_name(self) -> str:
        """ Returns the display name of the logged-in user. """
        return st.session_state.get("name", "User")

    @property
    def current_user_email(self) -> str:
        """ Returns the email address of the logged-in user. """
        return st.session_state.get("email", "")
