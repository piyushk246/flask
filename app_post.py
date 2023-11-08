# from flask import Flask, request, jsonify
# import json
# import os

# app = Flask(__name__)

# # Directory to store JSON files for different batteries
# data_directory = 'battery_data'

# # Ensure the data directory exists
# os.makedirs(data_directory, exist_ok=True)

# # Define a function to get the JSON file path for a battery
# def get_battery_file_path(battery_name):
#     return os.path.join(data_directory, f'{battery_name}.json')

# # Define API endpoint to store data for a specific battery
# @app.route('/api/battery/<battery_name>', methods=['POST'])
# def store_battery_data(battery_name):
#     try:
#         # Get the JSON file path for the specified battery
#         file_path = get_battery_file_path(battery_name)

#         # Get data from the request
#         data = request.json

#         # Validate data
#         if 'voltage' not in data or 'current' not in data or 'temperature' not in data:
#             return jsonify({"error": "Incomplete data. Please provide voltage, current, and temperature."}), 400

#         # Read existing data if the file exists
#         if os.path.exists(file_path):
#             with open(file_path, 'r') as file:
#                 existing_data = json.load(file)
#         else:
#             existing_data = []

#         # Append new data and save to the JSON file
#         existing_data.append(data)
#         with open(file_path, 'w') as file:
#             json.dump(existing_data, file, indent=4)
        
#         return jsonify({"message": "Data added successfully"}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run()
# =================== all working proper=============

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Directory to store JSON files for different batteries
data_directory = 'battery_data'

# Ensure the data directory exists
os.makedirs(data_directory, exist_ok=True)

# Define a function to get the JSON file path for a battery
def get_battery_file_path(battery_name):
    return os.path.join(data_directory, f'{battery_name}.json')

# Root route to display a message
@app.route('/')
def hello():
    return "Hello dear"
@app.route("/h")
def index():
    return "<h1>Hello!</h1>"
# @app.route('/ap', methods=['GET'])
# def hello():
#     return "Hello bc"
# Define API endpoint to store data for a specific battery
@app.route('/api/battery/<battery_name>', methods=['POST'])
def store_battery_data(battery_name):
    try:
        # Get the JSON file path for the specified battery
        file_path = get_battery_file_path(battery_name)

        # Get data from the request
        data = request.json

        # Validate data
        if 'voltage' not in data or 'current' not in data or 'temperature' not in data:
            return jsonify({"error": "Incomplete data. Please provide voltage, current, and temperature."}), 400

        # Read existing data if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []

        # Append new data and save to the JSON file
        existing_data.append(data)
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)
        
        return jsonify({"message": "Data added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port= 5000)