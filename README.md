# Investment Dashboard

A live dashboard to track mutual fund portfolio, NAVs, gain/loss, SWP, and reminders. Built using Streamlit and AMFI API.

## Features
- Auto-refresh every 15 minutes
- Live AMFI NAV integration
- Asset-wise gain/loss tracking
- SWP simulator
- Reminders and export to CSV

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Deployment
Deploy this app on [Streamlit Cloud](https://share.streamlit.io) by connecting your GitHub repo and selecting `dashboard.py`.
