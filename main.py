import json
from flask import Flask, render_template, request
# from matplotlib.figure import Figure
from io import BytesIO
import base64
app = Flask(__name__)


        
@app.route('/')
def index():
    return render_template('test.html')
    
# def load_data_from_json(battery_no):
#     file_path = f"battery_data/battery{battery_no}.json"
#     try:
#         with open(file_path, 'r') as file:
#             data = json.load(file)
#         return data
#     except (FileNotFoundError, json.JSONDecodeError):
        # return []

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=false)
