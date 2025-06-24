import streamlit as st
from urllib.parse import urlencode
import requests
import os
import time

# Load secrets
AUTH0_DOMAIN = st.secrets["auth0_domain"]
AUTH0_CLIENT_ID = st.secrets["auth0_client_id"]
AUTH0_CLIENT_SECRET = st.secrets["auth0_client_secret"]
AUTH0_REDIRECT_URI = st.secrets["auth0_redirect_uri"]
AUTH0_AUDIENCE = st.secrets.get("auth0_audience", f"https://{AUTH0_DOMAIN}/userinfo")

# Helper to get user info
def get_user_info(access_token):
    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    return response.json()

# Main logic
st.set_page_config(page_title="Magic Link Login", page_icon="🔐")
st.title("🔐 Streamlit + Auth0 OTP login")


if "email" not in st.session_state:
    with st.form("email_form", clear_on_submit=True):
        email = st.text_input("📧 Enter your email")
        submitted = st.form_submit_button("Send Login Code")
        if submitted and email:
            res = requests.post(
                f"https://{AUTH0_DOMAIN}/passwordless/start",
                json={
                    "client_id": AUTH0_CLIENT_ID,
                    "connection": "email",
                    "email": email,
                    "send": "code"
                }
            )
            if res.status_code == 200:
                st.success("✅ Check your inbox for the code.")
                st.session_state["email"] = email
                st.session_state["email_sent_time"] = time.time()
                st.rerun()
            else:
                st.error("❌ Failed to send code.")

elif "user" not in st.session_state:
    if time.time() - st.session_state.get("email_sent_time", 0) > 300:
        st.warning("⏰ Session expired.")
        if st.button("Resend Code"):
            del st.session_state["email"]
            st.rerun()
        st.stop()
    code = st.text_input("🔢 Enter the 6-digit code")
    if code:
        res = requests.post(
            f"https://{AUTH0_DOMAIN}/oauth/token",
            json={
                "grant_type": "http://auth0.com/oauth/grant-type/passwordless/otp",
                "client_id": AUTH0_CLIENT_ID,
                "client_secret": AUTH0_CLIENT_SECRET,
                "username": st.session_state["email"],
                "otp": code,
                "realm": "email",
                "scope": "openid profile email"
            }
        )
        if res.status_code == 200:
            token = res.json().get("access_token")
            st.session_state["user"] = get_user_info(token)
            st.rerun()
        else:
            st.error("❌ Invalid code.")

if "user" in st.session_state:
    user = st.session_state["user"]
    st.success(f"Welcome, {user.get('name', user.get('email'))}!")
    if st.button("Log out"):
        st.session_state.clear()
        st.rerun()