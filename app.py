from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np
import PIL
# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import image_utils
# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from flask import request

# Define a flask app
app = Flask(__name__)



def model_predict(img_path, model):
    img = image_utils.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image_utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

model= load_model("model/model.h5")

cache={}

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        print(cache)
        # Make prediction
        preds = model_predict(file_path,model)
        
        os.remove(file_path)
        
        cache['confidence_0'] = preds[0][0]
        cache['confidence_1'] = preds[0][1]
        # Process your result for human
        pred_class = preds.argmax(axis=-1)         
        
        if pred_class == 1:
            result = 'Pneumonia'
        else:
            result = 'Normal'
        print(result)
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)

