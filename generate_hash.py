#!/usr/bin/env python3
"""
SamiX Admin Password Hash Generator

This utility is used to generate a secure bcrypt hash for the administrative password.
The resulting hash should be placed in the `.streamlit/secrets.toml` file to enable
protected access to the Admin Panel.

Steps:
1. Run this script.
2. Enter your desired password twice to confirm.
3. Copy the hash starting with $2b$... and paste it into `secrets.toml`.
"""
import getpass
import bcrypt


def main() -> None:
    print("\nSamiX Password Hash Generator")
    # Prompt for the password securely without echoing characters.
    password = getpass.getpass("Enter the admin password: ")
    confirm  = getpass.getpass("Confirm password: ")

    if password != confirm:
        print("❌  Passwords do not match. Try again.")
        return

    # Generate a salt and hash the password using bcrypt (standard 12 rounds).
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12))
    
    print(f"\n✅  Paste this into `.streamlit/secrets.toml` → [auth] hashed_password:\n")
    print(f"    {hashed.decode('utf-8')}\n")


if __name__ == "__main__":
    main()
