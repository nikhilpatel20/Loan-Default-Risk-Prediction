import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"  # change after deploy

st.set_page_config(page_title="Loan Default Risk Predictor")

st.title("🏦 Loan Default Risk Prediction")

income = st.number_input("Income", min_value=0)
age = st.number_input("Age", min_value=18)
experience = st.number_input("Experience", min_value=0)

marital = st.selectbox("Marital Status", ["single", "married"])
house = st.selectbox("House Ownership", ["rented", "owned"])
car = st.selectbox("Car Ownership", ["no", "yes"])

profession = st.text_input("Profession", "Software_Developer")
state = st.text_input("State", "Madhya_Pradesh")

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

    res = requests.post(API_URL, json=payload)

    if res.status_code == 200:
        out = res.json()
        st.success(out["status"])
        st.write("Probability:", round(out["default_probability"], 3))
    else:
        st.error(res.text)


