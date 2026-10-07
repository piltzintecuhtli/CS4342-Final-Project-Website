# various helper functions to keep main.py clean

import main
import joblib
from os import path
import pandas as pd

def format_data(data):
    # formatting data for model input

    # input format
    #         all_data = [amt_usd, is_foreign_transaction, hrs_since_last_trnsctn, trnsctn_count_past_24_hrs,
    #                     distance_from_home_km, card_age, cust_age, acct_bal, is_new_merch,
    #                     used_vpn, ip_country_mismatch, billing_shipping_mismatch, cvv_retry_count, velocity_score,
    #                     time_of_day_hour, day_of_week, ai_scam_attempt, merchant_risk_score, prior_disputes,
    #                     merchant_category, card_type, auth_method, channel, device_type]

    # extract hour from time of day

    data[14] = data[14].hour
    data[15] = main.days_of_week.index(data[15])
    formatted_data = data[:19]

    merch_cat = value_to_one_hot(data[19], main.merchant_categories)
    card_type = value_to_one_hot(data[20], main.card_types)
    auth_method = value_to_one_hot(data[21], main.auth_methods)
    channel = value_to_one_hot(data[22], main.channels)
    device_type = value_to_one_hot(data[23], main.device_types)

    formatted_data = formatted_data + merch_cat + card_type + auth_method + channel + device_type

    cols_dict = {'amount_usd': formatted_data[0],
                 'is_foreign_transaction': formatted_data[1],
                 'hours_since_last_txn': formatted_data[2],
                 'txn_count_last_24h': formatted_data[3],
                 'distance_from_home_km': formatted_data[4],
                 'card_age_months': formatted_data[5],
                 'customer_age': formatted_data[6],
                 'account_balance_usd': formatted_data[7],
                 'is_new_merchant': formatted_data[8],
                 'used_vpn': formatted_data[9],
                 'ip_country_mismatch': formatted_data[10],
                 'billing_shipping_mismatch': formatted_data[11],
                 'cvv_retry_count': formatted_data[12],
                 'velocity_score': formatted_data[13],
                 'time_of_day_hour': formatted_data[14],
                 'day_of_week': formatted_data[15],
                 'is_ai_generated_scam_attempt': formatted_data[16],
                 'merchant_risk_score': formatted_data[17],
                 'prior_disputes': formatted_data[18],
                 'merchant_category_Crypto Exchange': formatted_data[19],
                 'merchant_category_Electronics': formatted_data[20],
                 'merchant_category_Fuel': formatted_data[21],
                 'merchant_category_Gaming': formatted_data[22],
                 'merchant_category_Gift Cards': formatted_data[23],
                 'merchant_category_Groceries': formatted_data[24],
                 'merchant_category_Healthcare': formatted_data[25],
                 'merchant_category_Online Retail': formatted_data[26],
                 'merchant_category_Restaurants': formatted_data[27],
                 'merchant_category_Streaming': formatted_data[28],
                 'merchant_category_Travel': formatted_data[29],
                 'merchant_category_Utilities': formatted_data[30],
                 'card_type_Amex': formatted_data[31],
                 'card_type_Discover': formatted_data[32],
                 'card_type_Mastercard': formatted_data[33],
                 'card_type_RuPay': formatted_data[34],
                 'card_type_Visa': formatted_data[35],
                 'auth_method_3D Secure': formatted_data[36],
                 'auth_method_Biometric': formatted_data[37],
                 'auth_method_No Authentication': formatted_data[38],
                 'auth_method_OTP': formatted_data[39],
                 'auth_method_PIN': formatted_data[40],
                 'channel_ATM': formatted_data[41],
                 'channel_Contactless': formatted_data[42],
                 'channel_In-App': formatted_data[43],
                 'channel_Online': formatted_data[44],
                 'channel_POS': formatted_data[45],
                 'device_type_ATM Machine': formatted_data[46],
                 'device_type_Android Phone': formatted_data[47],
                 'device_type_Mac': formatted_data[48],
                 'device_type_POS Terminal': formatted_data[49],
                 'device_type_Smart Watch': formatted_data[50],
                 'device_type_Tablet': formatted_data[51],
                 'device_type_Windows PC': formatted_data[52],
                 'device_type_iPhone': formatted_data[53]
                 }

    df = pd.DataFrame(cols_dict, index=[0])

    return df
    # desired format:
    # amt_usd, is_foreign_transaction, hrs_since_last_trnsctn, trnsctn_count_past_24_hrs
    # distance_from_home_km, card_age, cust_age, acct_bal, is_new_merch,
    # used_vpn, ip_country_mismatch, billing_shipping_mismatch, cvv_retry_count, velocity_score
    # time_of_day_hour, day_of_week, is_ai_generated_scam_attempt, merchant_risk_score, prior_disputes

    # merchant_category_Electronics
    # merchant_category_Fuel
    # merchant_category_Gaming
    # merchant_category_Gift Cards
    # merchant_category_Groceries
    # merchant_category_Healthcare
    # merchant_category_Online Retail
    # merchant_category_Restaurants
    # merchant_category_Streaming
    # merchant_category_Travel
    # merchant_category_Utilities

    # card_type_Discover
    # card_type_Mastercard
    # card_type_RuPay
    # card_type_Visa

    # auth_method_Biometric
    # auth_method_No Authentication
    # auth_method_OTP
    # auth_method_PIN

    # channel_Contactless
    # channel_In-App
    # channel_Online
    # channel_POS

    # device_type_Android Phone
    # device_type_Mac
    # device_type_POS Terminal
    # device_type_Smart Watch
    # device_type_Tablet
    # device_type_Windows PC
    # device_type_iPhone

def value_to_one_hot(value, array):
    tmp_array = [0] * len(array)
    tmp_array[array.index(value)] = 1

    return tmp_array


def scale_data(data):
    num_cols = ["amount_usd", "hours_since_last_txn", "txn_count_last_24h", "distance_from_home_km",
                "card_age_months", "customer_age", "account_balance_usd", "cvv_retry_count",
                "velocity_score", "time_of_day_hour", "day_of_week", "merchant_risk_score", "prior_disputes"]

    scaler = joblib.load(path.join("model_data", "scaler.pkl"))
    scaled_data = scaler.transform(data[num_cols])
    return scaled_data

def run_model(data):
    model = joblib.load(path.join("model_data", "log_reg_model.pkl"))
    pred = model.predict(data)
    prob = model.predict_proba(data)[:1]
    return pred, prob