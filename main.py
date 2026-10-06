import streamlit as st

st.header(":rainbow[Welcome to the Credit Card Fraud Detector 🕵️]")
st.subheader("Please enter the details of your transaction below and choose a model to calculate the chance of fraud")

st.divider()

model = st.selectbox("Choose a model", ["Logistic Regression"])

st.divider()

