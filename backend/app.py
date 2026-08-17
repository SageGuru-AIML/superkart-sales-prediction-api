import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask app
superkart_api = Flask("SuperKart Sales Predictor")

# Load the trained SuperKart sales prediction pipeline
model = joblib.load("superkart_model.joblib")

# Define a route for the home page
@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

# Define an endpoint to predict sales for a single product-store combination
@superkart_api.post('/v1/predict')
def predict_sales():
    # Get JSON data from the request
    product_data = request.get_json()

    # Extract the model features from the input data
    sample = {
        'Product_Weight': product_data['Product_Weight'],
        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_MRP': product_data['Product_MRP'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
        'Store_Type': product_data['Store_Type'],
        'Product_Id_char': product_data['Product_Id_char'],
        'Store_Age_Years': product_data['Store_Age_Years'],
        'Product_Type_Category': product_data['Product_Type_Category']
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a prediction using the trained pipeline
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Sales': round(prediction, 2)})

# Define an endpoint to predict sales for a batch of products
@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the uploaded file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch
    predictions = model.predict(input_data).tolist()

    # Return predictions keyed by row index as a JSON response
    return jsonify({str(i): round(p, 2) for i, p in enumerate(predictions)})

# Run the Flask app in debug mode
if __name__ == '__main__':
    superkart_api.run(debug=True)
