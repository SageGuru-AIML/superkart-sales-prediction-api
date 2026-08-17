import streamlit as st
import requests
import pandas as pd

# Setting the page configuration
st.set_page_config(page_title="SuperKart Sales Prediction", layout="wide")

# Title and description of the app
st.title("SuperKart Sales Prediction")
st.write(
    "This app predicts the sales revenue of a product in a SuperKart store. "
    "Use the form below for a single prediction or upload a CSV file for batch predictions."
)

# Backend API URL, reachable via the Docker network where the backend container is named 'backend'
backend_url = "http://backend:7860"

# ---------------- Online (single) prediction ----------------
st.header("Online Prediction")

# Numerical inputs
product_weight = st.number_input("Product Weight", min_value=1.0, max_value=30.0, value=12.66)
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.001, max_value=0.5, value=0.027, format="%.3f")
product_mrp = st.number_input("Product MRP", min_value=10.0, max_value=300.0, value=117.08)
store_age_years = st.number_input("Store Age (Years)", min_value=0, max_value=50, value=16)

# Categorical inputs
product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox(
    "Store Type",
    ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"],
)
product_id_char = st.selectbox("Product Id Prefix", ["FD", "DR", "NC"])
product_type_category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

# Collecting the inputs into the payload expected by the API
payload = {
    "Product_Weight": product_weight,
    "Product_Sugar_Content": product_sugar_content,
    "Product_Allocated_Area": product_allocated_area,
    "Product_MRP": product_mrp,
    "Store_Size": store_size,
    "Store_Location_City_Type": store_location_city_type,
    "Store_Type": store_type,
    "Product_Id_char": product_id_char,
    "Store_Age_Years": store_age_years,
    "Product_Type_Category": product_type_category,
}

# Sending the request to the backend when the button is clicked
if st.button("Predict Sales"):
    response = requests.post(backend_url + "/v1/predict", json=payload)
    if response.status_code == 200:
        prediction = response.json()["Sales"]
        st.success(f"Predicted Sales Revenue: {prediction}")
    else:
        st.error("Error connecting to the prediction API. Please try again.")

# ---------------- Batch prediction ----------------
st.header("Batch Prediction")

# Uploading a CSV file with the required feature columns
uploaded_file = st.file_uploader("Upload a CSV file with the required feature columns", type=["csv"])

if uploaded_file is not None and st.button("Predict Batch Sales"):
    batch_input = {"file": uploaded_file.getvalue()}
    response = requests.post(backend_url + "/v1/predictbatch", files=batch_input)
    if response.status_code == 200:
        predictions = response.json()
        batch_df = pd.read_csv(uploaded_file)
        batch_df["Predicted_Sales"] = [predictions[str(i)] for i in range(len(batch_df))]
        st.write("Predictions:")
        st.dataframe(batch_df)
    else:
        st.error("Error connecting to the prediction API. Please try again.")
