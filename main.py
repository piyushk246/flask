import json
from flask import Flask, render_template, request
# from matplotlib.figure import Figure
from io import BytesIO
import base64
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')
# @app.route('/h')
# def index1():
#     return "hello dear"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=false)
