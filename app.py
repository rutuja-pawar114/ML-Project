import streamlit as st
import pickle
import pandas as pd

# Load the pre-trained model
model = pickle.load(open("random_forest_regressor.pkl", "rb"))

# Function to predict the flight price
def predict_price(dep_time, arrival_time, stops, airline, source, destination):
    # Extracting features from the input data
    date_dep = pd.to_datetime(dep_time)
    Journey_day = date_dep.day
    Journey_month = date_dep.month
    Dep_hour = date_dep.hour
    Dep_min = date_dep.minute

    date_arr = pd.to_datetime(arrival_time)
    Arrival_hour = date_arr.hour
    Arrival_min = date_arr.minute

    # Duration (absolute value of difference)
    dur_hour = abs(Arrival_hour - Dep_hour)
    dur_min = abs(Arrival_min - Dep_min)

    # Airline encoding
    airline_dict = {
        'Jet Airways': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'IndiGo': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Air India': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        'Multiple carriers': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        'SpiceJet': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        'Vistara': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        'GoAir': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        'Multiple carriers Premium economy': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        'Jet Airways Business': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        'Vistara Premium economy': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        'Trujet': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    }
    
    # Encoding the selected airline
    airline_encoded = airline_dict.get(airline, [0] * 11)

    # Source encoding
    source_dict = {
        'Delhi': [1, 0, 0, 0],
        'Kolkata': [0, 1, 0, 0],
        'Mumbai': [0, 0, 1, 0],
        'Chennai': [0, 0, 0, 1]
    }
    
    # Encoding the selected source
    source_encoded = source_dict.get(source, [0, 0, 0, 0])

    # Destination encoding
    destination_dict = {
        'Cochin': [1, 0, 0, 0, 0],
        'Delhi': [0, 1, 0, 0, 0],
        'New Delhi': [0, 0, 1, 0, 0],
        'Hyderabad': [0, 0, 0, 1, 0],
        'Kolkata': [0, 0, 0, 0, 1]
    }
    
    # Encoding the selected destination
    destination_encoded = destination_dict.get(destination, [0, 0, 0, 0, 0])

    # Preparing the input features for prediction
    features = [
        stops, Journey_day, Journey_month, Dep_hour, Dep_min, Arrival_hour, Arrival_min,
        dur_hour, dur_min
    ]
    
    # Predict the flight price
    prediction = model.predict([features])
    return round(prediction[0], 2)

# Streamlit UI components
st.title("Flight Price Prediction App")

# Inputs from the user
dep_time = st.text_input("Departure Time (YYYY-MM-DDTHH:MM)", "2025-06-01T14:30")
arrival_time = st.text_input("Arrival Time (YYYY-MM-DDTHH:MM)", "2025-06-01T17:00")
stops = st.selectbox("Total Stops", [0, 1, 2])
airline = st.selectbox("Airline", ['Jet Airways', 'IndiGo', 'Air India', 'Multiple carriers', 
                                  'SpiceJet', 'Vistara', 'GoAir', 'Multiple carriers Premium economy', 
                                  'Jet Airways Business', 'Vistara Premium economy', 'Trujet'])
source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])

# Prediction button
if st.button('Predict Flight Price'):
    price = predict_price(dep_time, arrival_time, stops, airline, source, destination)
    st.success(f"The predicted flight price is Rs. {price}")

