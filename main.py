from flask import Flask, request, jsonify
from datetime import datetime
from typing import Dict, Any

app = Flask(__name__)

data_store: Dict[str, Dict[str, Any]] = {}


class WeatherData:
    def __init__(self, temperature: float, pressure: float, humidity: float):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity


def validate_weather_data(data: Dict[str, Any]) -> bool:
    # Walidacja danych pogodowych
    if not (-50 <= data.get('temperature', 0) <= 50):
        return False
    if not (800 <= data.get('pressure', 0) <= 1100):
        return False
    if not (0 <= data.get('humidity', 0) <= 100):
        return False
    return True


@app.route('/weather', methods=['POST'])
def add_weather_data():
    data = request.json
    if validate_weather_data(data):
        timestamp = datetime.now().isoformat()
        data_store[timestamp] = {
            "temperature": data['temperature'],
            "pressure": data['pressure'],
            "humidity": data['humidity']
        }
        return jsonify({"message": "Weather data added successfully"}), 201
    else:
        return jsonify({"error": "Invalid weather data provided"}), 400


@app.route('/weather/<timestamp>', methods=['GET'])
def get_weather_data(timestamp):
    if timestamp in data_store:
        weather_data = data_store[timestamp]
        return jsonify({
            "timestamp": timestamp,
            "temperature": weather_data['temperature'],
            "pressure": weather_data['pressure'],
            "humidity": weather_data['humidity']
        })
    else:
        return jsonify({"error": "Weather data not found"}), 404


@app.route('/nearest_weather', methods=['GET'])
def get_nearest_weather_data():
    target_timestamp = request.args.get('timestamp')
    if not target_timestamp:
        return jsonify({"error": "Timestamp parameter is required"}), 400

    nearest_timestamp = min(data_store.keys(), key=lambda x: abs(
        datetime.fromisoformat(x) - datetime.fromisoformat(target_timestamp)))
    nearest_weather_data = data_store[nearest_timestamp]
    return jsonify({
        "timestamp": nearest_timestamp,
        "temperature": nearest_weather_data['temperature'],
        "pressure": nearest_weather_data['pressure'],
        "humidity": nearest_weather_data['humidity']
    })


if __name__ == '__main__':
    app.run(debug=True)
