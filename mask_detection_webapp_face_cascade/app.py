from flask import Flask, render_template, Response, send_file,request
import cv2
import numpy as np
import tensorflow as tf

from live_detection_face_cascade import live_detect_face_cascade
from flask_socketio import SocketIO, emit

from flask import Flask, jsonify, request 
from flask_cors import CORS
import base64
import os 
from PIL import Image
from io import BytesIO

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
app.jinja_env.auto_reload = True

SocketIO = SocketIO(app, cors_allowed_origins="*")


app.config['SECRET_KEY'] = 'secret!'

# load the machine learning model in the app before runnning
model_loc = "my_model"
model = tf.keras.models.load_model(model_loc)

def generate_data():
    for i in range(10):
        yield i
        
# Assuming SocketIO is already initialized
@SocketIO.on('connect')
def handle_connect():
    print(f"Client connected, IP: {request.remote_addr}")

@SocketIO.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected, IP: {request.remote_addr}")

@SocketIO.on('frame')
def handle_message(data):
    # get the base64 of image data less the image header
    parts = data.split(',')[-1]

    # Create an image object from the decoded bytes
    image_bytes = base64.b64decode(parts)
    
    image = Image.open(BytesIO(image_bytes))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    try:
        processed_image_data = live_detect_face_cascade(model, image, process_frame=True)  
        for processed_frame in processed_image_data:
            # Assuming 'processed_frame' is the binary data of the processed image
            emit('processed_frame', {'image_data': base64.b64encode(processed_frame).decode('utf-8')}, cache_timeout=0)
            print("message emitted ")
    except Exception as e:
        print("An error occurred:", e)

@app.route('/')
def index():
    server_ip = request.headers.get('Host').split(':')[0]
    print(server_ip)
    os.environ['SERVER_IP'] = server_ip
    return render_template('index.html', server_ip=server_ip)


if __name__ == '__main__':
    SocketIO.run(app, host='0.0.0.0',port=8001)
