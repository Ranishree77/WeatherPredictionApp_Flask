from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    
    if not city:
        return jsonify({'error': 'City is required'}), 400
    
    current_weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'
    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}'
    
    try:
        current_response = requests.get(current_weather_url)
        current_data = current_response.json()

        if current_data['cod'] != 200:
            return jsonify({'error': current_data.get('message', 'City not found')}), 404

        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        weather_data = {
            'location': current_data['name'],
            'temperature': f"{current_data['main']['temp']}°C",
            'weather': current_data['weather'][0]['description'],
            'humidity': f"{current_data['main']['humidity']}%",
            'wind_speed': f"{current_data['wind']['speed']} m/s",
            'forecast': []
        }

        for entry in forecast_data['list']:
            weather_data['forecast'].append({
                'date': entry['dt_txt'],
                'temperature': f"{entry['main']['temp']}°C",
                'weather': entry['weather'][0]['description']
            })

        return jsonify(weather_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
