from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

api_key = '09de91caf3b6d3d1c4739bf430ece1a2'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    user_input = request.args.get('city')
    if not user_input:
        return jsonify({"error": "City is required"}), 400

    daily = 'current'
    
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={api_key}&exclude={daily}")

    if weather_data.status_code == 404:
        return jsonify({"error": "City not found"}), 404

    weather = weather_data.json()['weather'][0]['main']
    rain = round(float(weather_data.json().get('rain', {}).get('1h', 0)), 3)

    precipitation = rain * 24

    if 70 <= precipitation <= 101:
        flood_warning = "There is a possibility of flooding"
    elif precipitation >= 102:
        flood_warning = "Floods are sure to happen"
    else:
        flood_warning = "Normal"

    return jsonify({
        "city": user_input,
        "weather": weather,
        "precipitation": f"{precipitation} mm/24h",
        "flood_warning": flood_warning
    })

if __name__ == '__main__':
    app.run(debug=True)
