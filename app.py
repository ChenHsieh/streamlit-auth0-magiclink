import streamlit as st
from urllib.parse import urlencode
import requests
import os

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
st.title("🔐 Streamlit + Auth0 Magic Link")

# Replace magic link form with code-based flow
email = st.text_input("Enter your email to receive a login code:")
if st.button("Send Login Code") and email:
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "connection": "email",
        "email": email,
        "send": "code",
    }
    response = requests.post(f"https://{AUTH0_DOMAIN}/passwordless/start", json=payload)
    st.text(f"Status Code: {response.status_code}")
    st.text(f"Response: {response.text}")
    if response.status_code == 200:
        st.success("✅ Login code sent! Check your inbox.")
    else:
        st.error("❌ Failed to send login code. Double-check your Auth0 configuration.")

# Prompt for verification code
verification_code = st.text_input("Enter the 6-digit login code from your email:")

if "user" not in st.session_state and verification_code and email:
    token_payload = {
        "grant_type": "http://auth0.com/oauth/grant-type/passwordless/otp",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "username": email,
        "otp": verification_code,
        "realm": "email",
        "scope": "openid profile email",
    }
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    token_response = requests.post(token_url, json=token_payload)
    st.text(f"Token Status: {token_response.status_code}")
    st.text(f"Token Response: {token_response.text}")
    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if access_token:
            user = get_user_info(access_token)
            st.session_state["user"] = user

if "user" not in st.session_state:
    st.stop()

# Authenticated user content
user = st.session_state["user"]
st.success(f"Welcome, {user.get('name', user.get('email'))}!")

if st.button("Log out"):
    st.session_state.clear()
    st.experimental_rerun()