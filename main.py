import streamlit as st
import helpers

# array constants
merchant_categories = ["Crypto Exchange", "Electronics", "Fuel", "Gaming", "Gift Cards", "Groceries", "Healthcare", "Online Retail", "Restaurants", "Streaming", "Travel", "Utilities"]
card_types = ["Amex", "Discover", "Mastercard", "RuPay", "Visa"]
auth_methods = ["3D Secure", "Biometric", "No Authentication", "OTP", "PIN"]
channels = ["ATM", "Contactless", "In-App", "Online", "POS"]
device_types = ["ATM Machine", "Android Phone", "Mac", "POS Terminal", "Smart Watch", "Tablet", "Windows PC", "iPhone"]
days_of_week = ["Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday"]
num_cols = ["amount_usd", "hours_since_last_txn", "txn_count_last_24h", "distance_from_home_km",
                "card_age_months", "customer_age", "account_balance_usd", "cvv_retry_count",
                "velocity_score", "time_of_day_hour", "day_of_week", "merchant_risk_score", "prior_disputes"]

calculated = False
pred, prob = 0, 0

st.header(":rainbow[🕵️ Welcome to the Credit Card Fraud Detector 🕵️]")
st.subheader("Please enter the details of your transaction below and choose a model to calculate the chance of fraud")

st.divider()

model = st.selectbox("Choose a model", ["Logistic Regression"], key="sb-models")

st.divider()

with st.form("Transaction Details"):
    st.subheader("Transaction Details")
    amt_usd = st.number_input("Purchase amount (USD)", min_value=0.0, value=0.0, step=0.01,
                              key="ni-txn-amt")
    auth_method = st.pills("Authentication method", auth_methods, key="p-auth-method")
    channel = st.pills("Channel", channels, key="p-chan")
    device_type = st.pills("Device type", device_types, key="p-device-type")
    is_foreign_transaction = st.checkbox("Foreign transaction", False, key="check-foreign")
    # TODO: change km to be km or miles
    distance_from_home_km = st.number_input("Distance from home address the transaction made", 0, value=0,
                                            key="number-dist")
    used_vpn = st.checkbox("VPN used", False, key="check-use-vpn")
    ip_country_mismatch = not (
        st.checkbox("Does the IP when purchasing match the user's country?", False, key="check-ip-match"))
    billing_shipping_mismatch = not (
        st.checkbox("Do the billing and shipping addresses match?", False, key="check-shipping-match"))
    cvv_retry_count = st.number_input("CVV retry times", 0, value=0, key="number-cvv-retry")
    # TODO: potentially combine into one question
    time_of_day_hour = st.time_input("At what time did the purchase occur?", key="time-time-hour")
    day_of_week = st.selectbox("Day of the week", days_of_week, key="select-day-of-week")

    st.divider()
    st.subheader("Account and Card Details")
    card_type = st.pills("Card type", card_types, key="p-card-type")
    hrs_since_last_trnsctn = st.number_input("Hours since the card's last transaction", 0, value=0,
                                             key="number-hr-last-transaction")
    trnsctn_count_past_24_hrs = st.number_input("Number of transactions in the past 24 hours", 0, value=0,
                                                key="number-trns-count")
    card_age = st.number_input("In months, how old was the card?", 0, value=0, key="number-card")
    cust_age = st.number_input("How old was the customer?", 0, value=0, key="number-cust")
    acct_bal = st.number_input("What was the customer's account balance?", 0, value=0, key="number-acct")
    prior_disputes = st.number_input("Number of prior disputes", 0, value=0, key="number-prior")

    st.divider()
    st.subheader("Merchant Details")
    merchant_category = st.selectbox("Merchant category", merchant_categories, key="sb-merch-cat")
    is_new_merch = st.checkbox("Was the merchant new at the time of purchase?", False, key="check-new-merch")
    merchant_risk_score = st.number_input("Merchant risk score", 0.0, 100.0, value=0.0, step=0.1, key="number-risk")

    velocity_score = st.number_input("Velocity Score - idk what this is", 0, value=0, key="number-velocity-score")
    ai_scam_attempt = st.checkbox("AI scam attempt?", False, key="check-ai-scam-attempt")

    submitted = st.form_submit_button("Submit")
    if submitted:
        if merchant_category is None or card_type is None or channel is None or device_type is None:
            st.write("Please ensure all fields have been filled out!")

        else:
            calculated = False
            all_data = [amt_usd, is_foreign_transaction, hrs_since_last_trnsctn, trnsctn_count_past_24_hrs,
                    distance_from_home_km, card_age, cust_age, acct_bal, is_new_merch,
                    used_vpn, ip_country_mismatch, billing_shipping_mismatch, cvv_retry_count, velocity_score,
                    time_of_day_hour, day_of_week, ai_scam_attempt, merchant_risk_score, prior_disputes,
                    merchant_category, card_type, auth_method, channel, device_type]
            all_data = helpers.format_data(all_data)
            all_data[num_cols] = helpers.scale_data(all_data)
            pred, prob = helpers.run_model(all_data)

            calculated = True

if calculated:
    if pred:
        st.write(":red[This transaction was likely fraudulent!]")
    else:
        st.write(":rainbow[This transaction was likely NOT fraudulent :D!]")

    st.write("Probability of being a fraudulent transaction: " + str(round(prob.item(0), 5)))
    st.write("Probability of being a real transaction: " + str(round(prob.item(1), 5)))