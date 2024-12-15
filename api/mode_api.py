import os
from dotenv import load_dotenv
from flask import Blueprint, jsonify, current_app
import requests

mode_api = Blueprint('mode_api', __name__)
load_dotenv()
ESP32_IP = os.getenv('ESP32_IP')

@mode_api.route("/fan/mode/automatic", methods=["POST"])
def set_fan_automatic():
    try:
        url = f"http://{ESP32_IP}/fan/automatic"
        payload = {'status': 'on'}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return jsonify({
            "message": "Fan automatic mode is ON",
            "esp_response": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mode_api.route("/fan/mode/manual", methods=["POST"])
def set_fan_manual():
    try:
        url = f"http://{ESP32_IP}/fan/automatic"
        payload = {'status': 'off'}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return jsonify({
            "message": "Fan manual mode is OFF",
            "esp_response": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mode_api.route("/pump/mode/automatic", methods=["POST"])
def set_pump_automatic():
    try:
        url = f"http://{ESP32_IP}/pump/automatic"
        payload = {'status': 'on'}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return jsonify({
            "message": "Pump automatic mode is ON",
            "esp_response": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mode_api.route("/pump/mode/manual", methods=["POST"])
def set_pump_manual():
    try:
        url = f"http://{ESP32_IP}/pump/automatic"
        payload = {'status': 'off'}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return jsonify({
            "message": "Pump manual mode is OFF",
            "esp_response": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mode_api.route("/curtain/mode/automatic", methods=["POST"])
def set_curtain_automatic():
    try:
        url = f"http://{ESP32_IP}/curtain/automatic"
        payload = {'status': 'on'}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return jsonify({
            "message": "Curtain automatic mode is ON",
            "esp_response": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mode_api.route("/curtain/mode/manual", methods=["POST"])
def set_curtain_manual():
    try:
        url = f"http://{ESP32_IP}/curtain/automatic"
        payload = {'status': 'off'}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return jsonify({
            "message": "Curtain manual mode is OFF",
            "esp_response": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mode_api.route("/light/mode/automatic", methods=["POST"])
def set_led_automatic():
    try:
        url = f"http://{ESP32_IP}/led/automatic"
        payload = {'status': 'on'}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return jsonify({
            "message": "LED automatic mode is ON",
            "esp_response": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mode_api.route("/light/mode/manual", methods=["POST"])
def set_led_manual():
    try:
        url = f"http://{ESP32_IP}/led/automatic"
        payload = {'status': 'off'}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        current_app.config['automaticLight'] = False
        return jsonify({
            "message": "LED manual mode is OFF",
            "esp_response": response.json()
        }), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500