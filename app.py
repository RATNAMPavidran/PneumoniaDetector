from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np
import PIL
import tensorflow 

from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.utils import image_utils

from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from flask import request


app = Flask(__name__)



def model_predict(img_path, model):
    img = image_utils.load_img(img_path, target_size=(224, 224))

   
    x = image_utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    
    return render_template('index.html')

model= load_model("model/model.h5")

cache={}

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    print("test")
    if request.method == 'POST':
        print("test")
        f = request.files['file']

       
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        file_path = os.path.abspath(file_path)
        f.save(file_path)
        print(cache)
        
        preds = model_predict(file_path,model)
        
        os.remove(file_path)
        
        cache['confidence_0'] = preds[0][0]
        cache['confidence_1'] = preds[0][1]
        
        
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

