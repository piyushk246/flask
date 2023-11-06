import json
from flask import Flask, render_template, request
from matplotlib.figure import Figure
from io import BytesIO
import base64

app = Flask(__name__)

# Function to load data from a JSON file
def load_data_from_json(battery_no):
    file_path = f"battery_data/battery{battery_no}.json"
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

    fig = Figure(figsize=(8, 6))
    ax = fig.subplots(3, 1, sharex=True)
    voltage = [entry['voltage'] for entry in data]
    current = [entry['current'] for entry in data]
    temperature = [entry['temperature'] for entry in data]

    ax[0].plot(range(len(data)), voltage, label='Voltage')
    ax[1].plot(range(len(data)), current, label='Current')
    ax[2].plot(range(len(data)), temperature, label='Temperature')

    for i in range(3):
        ax[i].set_ylabel(['Voltage (V)', 'Current (A)', 'Temperature (°C)'][i])

    ax[2].set_xlabel('Data Point Index')

    for i in range(3):
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

@app.route('/plot', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        battery_no = int(request.form['battery_number'])
        image = update_plot(battery_no)
        if image:
            return render_template('test.html', battery_no=battery_no, image=image)
        return "No data available for battery " + str(battery_no)
    return render_template('test.html')

# Main route
@app.route('/')
def index():
    return  render_template('index1.html')
    # return "Enter a battery number in the URL to view the real-time plot."

if __name__ == "__main__":
    # app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=5000, debug=True)
