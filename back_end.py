from flask import Flask, request, jsonify, render_template
import requests
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

# Load the AI model and scaler at the start
loaded_svr_model = joblib.load('svr_rain.pickle')
loaded_scaler = joblib.load('scaler.pickle')

# API key for OpenWeatherMap
api_key = '09de91caf3b6d3d1c4739bf430ece1a2'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    # Get city name from request parameters
    user_input = request.args.get('city')

    if not user_input:
        return jsonify({'error': 'City name is required'}), 400

    # Fetch weather data
    daily = 'current'
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}&exclude={daily}"
    )
    
    if weather_data.status_code != 200:
        return jsonify({'error': 'City not found'}), 404

    weather_json = weather_data.json()

    # Extract weather information
    weather = weather_json['weather'][0]['main']
    rain = round(float(weather_json.get('rain', {}).get('1h', 0)), 3)
    precipitation = rain * 24

    new_data = {
        'precipitation': [precipitation],
        'water level': [0.8],  
        'Soil moisture': [100]  
    }
    new_df = pd.DataFrame(new_data)

    # Scale the data
    new_data_scaled = loaded_scaler.transform(new_df)

    # Predict flood risk
    new_predictions = loaded_svr_model.predict(new_data_scaled)
    flood_warning = "Yes" if new_predictions[0] >= 0.5 else "No"

    # Prepare 
    response = {
        "city": user_input,
        "weather": weather,
        "precipitation": f"{precipitation} mm/24h",
        "flood_warning": flood_warning
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
