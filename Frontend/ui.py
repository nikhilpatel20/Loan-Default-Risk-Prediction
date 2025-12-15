import streamlit as st
import requests
import os

# Render se API URL aana chahiye
API_URL = os.getenv("API_URL")

if API_URL is None:
    st.error("API_URL environment variable not set")
    st.stop()

st.set_page_config(page_title="Loan Default Risk Predictor")
st.title("🏦 Loan Default Risk Prediction")

income = st.number_input("Income", min_value=0)
age = st.number_input("Age", min_value=18)
experience = st.number_input("Experience", min_value=0)

marital = st.selectbox("Marital Status", ["single", "married"])
house = st.selectbox("House Ownership", ["rented", "owned"])
car = st.selectbox("Car Ownership", ["no", "yes"])

profession = st.text_input("Profession")
state = st.text_input("State")

job_yrs = st.number_input("Current Job Years", min_value=0)
house_yrs = st.number_input("Current House Years", min_value=0)

if st.button("Predict"):
    payload = {
        "Income": income,
        "Age": age,
        "Experience": experience,
        "Married/Single": marital,
        "House_Ownership": house,
        "Car_Ownership": car,
        "Profession": profession,
        "STATE": state,
        "CURRENT_JOB_YRS": job_yrs,
        "CURRENT_HOUSE_YRS": house_yrs,
    }

    try:
        res = requests.post(API_URL, json=payload)
        res.raise_for_status()
        out = res.json()
        st.success(out["status"])
        st.write("Probability:", round(out["default_probability"], 3))
    except Exception as e:
        st.error(f"API call failed: {e}")
