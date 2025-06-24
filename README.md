# streamlit-auth0-OTP

This is a minimal example of implementing passwordless authentication (OTP via email) in Streamlit using Auth0.

## Features

- Email-based one-time code (OTP) login using Auth0's passwordless API.
- Simple step-by-step Streamlit UI with email input and code verification.
- Session-based login with auto-expiration and logout support.

## Setup

1. Add your Auth0 credentials in `.streamlit/secrets.toml`:
    ```toml
    auth0_domain = "YOUR_AUTH0_DOMAIN"
    auth0_client_id = "YOUR_CLIENT_ID"
    auth0_client_secret = "YOUR_CLIENT_SECRET"
    auth0_redirect_uri = "http://localhost:8501"
    ```

2. Run the app:
    ```bash
    streamlit run app.py
    ```

## Notes

- Make sure the "email" passwordless connection is enabled in your Auth0 dashboard.
- The app is for development/demo use only. Use HTTPS and production settings for real deployments.