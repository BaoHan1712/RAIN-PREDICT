import requests
import pandas as pd
import numpy as np
import joblib

api_key = '09de91caf3b6d3d1c4739bf430ece1a2'

user_input = input("Enter City: ")

daily= 'current'

# weather_data = requests.get(
#     f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}&exclude={daily}")
 
weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}&exclude={daily}")  
    

weather = weather_data.json()['weather'][0]['main']
rain = round(float(weather_data.json().get('rain', {}).get('1h', 0)), 3)

precipitation = rain * 24

loaded_svr_model = joblib.load('svr_rain.pickle')

# Load scaler 
loaded_scaler = joblib.load('scaler.pickle')

new_data = {
    'precipitation': [precipitation],
    'water level': [1.4],
    'Soil moisture': [150]
}

new_df = pd.DataFrame(new_data)

# Chuẩn hóa data
new_data_scaled = loaded_scaler.transform(new_df)

# Predict
new_predictions = loaded_svr_model.predict(new_data_scaled)
binary_predictions = np.where(new_predictions >= 0.5, "Yes", "No")

print("Flood forecast:", binary_predictions)
print(" Predict % :", new_predictions)
