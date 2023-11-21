from flask import Flask, render_template, request, jsonify
from matplotlib.figure import Figure
from io import BytesIO
import base64
import json
import os

app = Flask(__name__)

# Directory to store JSON files for different batteries
data_directory = 'battery_data'

# Ensure the data directory exists
os.makedirs(data_directory, exist_ok=True)

# Define a function to get the JSON file path for a battery
def get_battery_file_path(battery_no):
    return os.path.join(data_directory, f'battery{battery_no}.json')

# Function to load data from a JSON file
def load_data_from_json(battery_no):
    file_path = get_battery_file_path(battery_no)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to update the plot
def update_plot(battery_no):
    data = load_data_from_json(battery_no)

    if not data:
        return None

    fig = Figure(figsize=(8, 8))  # Increase the figure size for the resistance plot
    ax = fig.subplots(4, 1, sharex=True)
    voltage = [entry['voltage'] for entry in data]
    current = [entry['current'] for entry in data]
    resistance = [voltage[i] / current[i] if current[i] != 0 else 0 for i in range(len(data))]
    temperature = [entry['temperature'] for entry in data]

    ax[0].plot(range(len(data)), voltage, label='Voltage')
    ax[1].plot(range(len(data)), current, label='Current')
    ax[2].plot(range(len(data)), resistance, label='Resistance')  # Add the resistance plot
    ax[3].plot(range(len(data)), temperature, label='Temperature')

    for i in range(4):
        ax[i].set_ylabel(['Voltage (V)', 'Current (A)', 'Resistance (Ω)', 'Temperature (°C)'][i])

    ax[3].set_xlabel('Data Point Index')

    for i in range(4):
        ax[i].set_title(f'Battery {battery_no} Data')
        ax[i].legend()

    fig.tight_layout()
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    fig.clf()

    return base64.b64encode(img.getvalue()).decode()

# Route to display the real-time plot
@app.route('/plot/<int:battery_no>')
def plot_battery(battery_no):
    image = update_plot(battery_no)
    if image:
        return render_template('index.html', battery_no=battery_no, image=image)
    return "No data available for battery " + str(battery_no)

# API endpoint to store data for a specific battery
@app.route('/api/battery/<int:battery_no>', methods=['POST'])
def store_battery_data(battery_no):
    try:
        # Get the JSON file path for the specified battery
        file_path = get_battery_file_path(battery_no)

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

# Route to display the initial page with a form
@app.route('/plot', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        battery_no = int(request.form['battery_number'])
        image = update_plot(battery_no)
        if image:
            return render_template('index.html', battery_no=battery_no, image=image)
        return "No data available for battery " + str(battery_no)
    return render_template('index.html')

# Main route
@app.route('/')
def index():
    return render_template('index1.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
