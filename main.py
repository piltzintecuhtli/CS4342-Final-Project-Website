import streamlit as st

merchant_categories = ["Restaurants", "Online Retail", "Groceries", "Streaming", "Travel", "Gift Cards", "Electronics", "Fuel", "Gaming", "Utilities", "Crypto Exchange", "Healthcare"]
card_types = ["Visa", "Mastercard", "Amex", "RuPay", "Discover"]
auth_methods = ["OTP", "3D Secure", "No Authentication", "Biometric", "PIN"]
channels = ["Online", "POS", "In-App", "Contactless", "ATM"]
device_types = ["Android Phone", "Mac", "iPhone", "POS Terminal", "ATM Machine", "Tablet", "Windows PC", "Smart Watch"]
days_of_week = ["Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday"]

st.header(":rainbow[🕵️ Welcome to the Credit Card Fraud Detector 🕵️]")
st.subheader("Please enter the details of your transaction below and choose a model to calculate the chance of fraud")

st.divider()

model = st.selectbox("Choose a model", ["Logistic Regression"])

st.divider()

amount_usd = st.number_input("In USD, how much was your purchase?", min_value=0.0, value=0.0, step=0.01)

merchant_category = st.selectbox("Merchant category", merchant_categories)

card_type = st.pills("Card type", card_types)

auth_method = st.pills("Authentication method", auth_methods)

channel = st.pills("Channel", channels)

device_type = st.pills("Device type", device_types)

is_foreign_transaction = st.checkbox("Was this transaction a foreign transaction?", False)

hrs_since_last_trnsctn = st.number_input("Hours since the card's last transaction", 0, value=0)

trnsctn_count_past_24_hrs  = st.number_input("Number of transactions in the past 24 hours", 0, value=0)

# TODO: change km to be km or miles
distance_from_home_km = st.number_input("How far away from home was the transaction made?", 0, value=0)

card_age = st.number_input("In months, how old was the card?", 0, value=0)

cust_age = st.number_input("How old was the customer?", 0, value=0)

acct_bal = st.number_input("What was the customer's account balance?", 0, value=0)

is_new_merch = st.checkbox("Was the merchant new at the time of purchase?", False)

used_vpn = st.checkbox("Was the transaction done using a VPN?", False)

ip_country_mismatch = not(st.checkbox("Does the IP when purchasing match the user's country?", False))

billing_shipping_mismatch = not(st.checkbox("Do the billing and shipping addresses match?", False))

cvv_retry_count = st.number_input("How many times was the card's CVV retried?", 0, value=0)

velocity_score = st.number_input("Velocity Score - idk what this is", 0, value=0)

time_of_day_hour = st.time_input("At what time did the purchase occur?")

day_of_week = st.selectbox("Day of the week", days_of_week)

ai_scam_attempt = st.checkbox("AI scam attempt?", False)

merchant_risk_score = st.number_input("Merchant risk score", 0.0, 100.0, value=0.0, step=0.1)

prior_disputes = st.number_input("Number of prior disputes", 0, value=0)