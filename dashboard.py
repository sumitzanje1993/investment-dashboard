
# Step 1: Import Libraries
import streamlit as st
import pandas as pd
import requests
import datetime
import plotly.express as px
import time

# Step 2: Define Sample Portfolio
portfolio = [
    {"Asset": "Parag Parikh Flexi Cap Fund", "AMFI Code": "120503", "Amount": 5000, "Type": "Equity"},
    {"Asset": "ICICI Infrastructure Fund", "AMFI Code": "120767", "Amount": 15000, "Type": "Thematic"},
    {"Asset": "Embassy Office Parks REIT", "Price": 335, "Units": 60, "Type": "REIT"},
    {"Asset": "ICICI Corporate Bond Fund", "AMFI Code": "118834", "Amount": 25000, "Type": "Debt"},
    {"Asset": "HDFC Balanced Advantage Fund", "AMFI Code": "118550", "Amount": 15000, "Type": "Hybrid"},
    {"Asset": "Axis Liquid Fund", "AMFI Code": "119551", "Amount": 5000, "Type": "Liquid"}
]

# Step 3: Function to fetch NAV from AMFI
def fetch_nav(amfi_code):
    try:
        url = "https://www.amfiindia.com/spages/NAVAll.txt"
        response = requests.get(url)
        response.encoding = 'utf-8'
        lines = response.text.split('\n')
        for line in lines:
            if line.startswith(str(amfi_code)):
                parts = line.strip().split(';')
                return float(parts[-2])
        return None
    except:
        return None

# Step 4: Compute Portfolio Value
def build_portfolio_df():
    data = []
    for asset in portfolio:
        if asset["Type"] == "REIT":
            value = asset["Price"] * asset["Units"]
            data.append({
                "Asset": asset["Asset"],
                "Type": asset["Type"],
                "Invested": asset["Price"] * asset["Units"],
                "Current Value": value,
                "Gain/Loss": 0
            })
        else:
            nav = fetch_nav(asset["AMFI Code"])
            if nav:
                units = asset["Amount"] / nav
                current_value = units * nav
                data.append({
                    "Asset": asset["Asset"],
                    "Type": asset["Type"],
                    "Invested": asset["Amount"],
                    "Current Value": round(current_value, 2),
                    "Gain/Loss": round(current_value - asset["Amount"], 2)
                })
    return pd.DataFrame(data)

# Step 5: Streamlit Dashboard Setup
st.set_page_config(page_title="Investment Dashboard", layout="wide")
st.title("Personal Investment Dashboard")

# Refresh every 15 mins
if 'last_refresh' not in st.session_state or (time.time() - st.session_state['last_refresh'] > 900):
    portfolio_df = build_portfolio_df()
    st.session_state['portfolio_df'] = portfolio_df
    st.session_state['last_refresh'] = time.time()
else:
    portfolio_df = st.session_state['portfolio_df']

# Sidebar Filters
st.sidebar.title("Filters")
selected_type = st.sidebar.multiselect("Filter by Asset Type", portfolio_df["Type"].unique(), default=portfolio_df["Type"].unique())
filtered_df = portfolio_df[portfolio_df["Type"].isin(selected_type)]

# Portfolio Summary
st.subheader("Portfolio Summary")
st.dataframe(filtered_df)

# Pie Chart
st.subheader("Allocation by Asset Type")
fig = px.pie(filtered_df, names="Type", values="Current Value", title="Asset Allocation")
st.plotly_chart(fig, use_container_width=True)

# Gain/Loss Chart
st.subheader("Gain/Loss by Asset")
fig2 = px.bar(filtered_df, x="Asset", y="Gain/Loss", color="Gain/Loss", title="Per Asset Gain/Loss", text="Gain/Loss")
st.plotly_chart(fig2, use_container_width=True)

# Step 6: SWP Simulator
st.subheader("SWP Simulator")
swp_corpus = st.number_input("Enter corpus amount (INR)", value=500000)
swp_amount = st.number_input("Monthly SWP amount (INR)", value=5000)
expected_return = st.slider("Expected Annual Return (%)", 0.0, 15.0, 10.0)

monthly_rate = (1 + expected_return/100)**(1/12) - 1
months = 0
balance = swp_corpus
while balance > 0 and months < 600:
    balance *= (1 + monthly_rate)
    balance -= swp_amount
    if balance < 0:
        balance = 0
    months += 1
st.write(f"\nYour corpus will last for **{months} months (~{months//12} years and {months%12} months)**.")

# Step 7: Reminder Panel
st.subheader("Reminders & Notes")
reminders = [
    "✅ Upcoming SIP Date: 10th of each month",
    "✅ SGB Next Window: Awaiting RBI Notification",
    "✅ Embassy REIT Q1 Payout: May 15, 2025",
    "🔁 Review portfolio quarterly",
    "📥 Top up ICICI Infra Fund if cash available"
]
for r in reminders:
    st.write(r)

# Step 8: Export Options
st.subheader("Export Portfolio Data")
export = st.button("Download Portfolio as CSV")
if export:
    csv = portfolio_df.to_csv(index=False).encode('utf-8')
    st.download_button("Click to Download", data=csv, file_name="portfolio_summary.csv", mime='text/csv')

# Footer
st.markdown("---")
st.markdown("Built by your financial assistant. Auto-refreshes every 15 minutes with live AMFI NAVs.")
