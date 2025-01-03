from flask import Blueprint, request, jsonify ,current_app
import requests
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from torch.distributed.argparse_util import env

sensor_api = Blueprint('sensor_api', __name__)
load_dotenv()
ESP32_IP = os.getenv('ESP32_IP')



@sensor_api.route('/data', methods=['GET'])
def get_data():
    try:
        response = requests.get(f"http://{ESP32_IP}/data")
        response.raise_for_status()
        data = response.json()
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


@sensor_api.route('/statistics', methods=['GET'])
def statistics():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    filter_type = request.args.get('filter_type', 'day')
    filter_value = request.args.get('filter_value', datetime.now().strftime('%Y-%m-%d'))

    try:
        if filter_type == 'day':
            start_value = datetime.strptime(filter_value, '%Y-%m-%d')
            end_value = start_value + timedelta(days=1)
            query = "SELECT * FROM sensor_status WHERE timestamp >= ? AND timestamp < ?"
            parameters = (start_value.strftime('%Y-%m-%d %H:%M:%S'), end_value.strftime('%Y-%m-%d %H:%M:%S'))
        elif filter_type == 'hour':
            start_value = datetime.strptime(filter_value.split('.')[0], '%Y-%m-%dT%H:%M:%S')
            end_value = start_value - timedelta(hours=1)
            query = "SELECT * FROM sensor_status WHERE timestamp >= ? AND timestamp < ?"
            parameters = (end_value.strftime('%Y-%m-%d %H:%M:%S'), start_value.strftime('%Y-%m-%d %H:%M:%S'))
        elif filter_type == 'month':
            start_value = datetime.strptime(filter_value, '%Y-%m-%d')
            end_value = (start_value + timedelta(days=32)).replace(day=1)
            query = "SELECT * FROM sensor_status WHERE timestamp >= ? AND timestamp < ?"
            parameters = (start_value.strftime('%Y-%m-01 00:00:00'), end_value.strftime('%Y-%m-01 00:00:00'))
        elif filter_type == 'week':
            start_value = datetime.strptime(filter_value, '%Y-%m-%d')
            start_value = start_value - timedelta(days=start_value.weekday())
            end_value = start_value + timedelta(days=7)
            query = "SELECT * FROM sensor_status WHERE timestamp >= ? AND timestamp < ?"
            parameters = (start_value.strftime('%Y-%m-%d %H:%M:%S'), end_value.strftime('%Y-%m-%d %H:%M:%S'))
        elif filter_type == 'year':
            start_value = datetime.strptime(filter_value, '%Y-%m-%d')
            start_value = start_value.replace(month=1, day=1)
            end_value = start_value.replace(year=start_value.year + 1)
            query = "SELECT * FROM sensor_status WHERE timestamp >= ? AND timestamp < ?"
            parameters = (start_value.strftime('%Y-%m-%d %H:%M:%S'), end_value.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            return jsonify({'error': 'Invalid filter type'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {str(e)}'}), 400

    cursor.execute(query, parameters)
    data = cursor.fetchall()

    def convert_values(row):
        return {
            'id': row[0],
            'timestamp': row[1],
            'humidity': float(row[2]),
            'temperature': float(row[3]),
            'soil_moisture': int(row[4]),
            'distance': int(row[5]),
            'pump_status': row[6],
            'light': int(row[7]),
            'waterLevel': int(row[8]),
            'sound_status': int(row[9]),
            'fanStatus': int(row[10]),
            'curtainStatus': int(row[11]),
            'automaticFan': int(row[12]),
            'automaticPump': int(row[13]),
            'automaticCurtain': int(row[14])
        }

    data = [convert_values(row) for row in data]

    conn.close()
    return jsonify(data)
