import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
import data_set
import model
import numpy as np

monkey.patch_all()
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU

model = model.FaceRecognitionModel("E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/super_parms2.properties")
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/hello')
def response_request():
    return "hi"


@app.route('/upload', methods=['POST'])
def upload():
    super_parms = model.super_parms
    imgs = request.files.getlist('data')
    input_height = int(super_parms.get("input_height"))
    input_width = int(super_parms.get("input_width"))
    input_channel = int(super_parms.get("input_channel"))
    label_length = int(super_parms.get("label_length"))
    input, label = data_set.read_data(imgs, input_height, input_width, input_channel, label_length)
    y_conv_, y_conv_max_ = model.predit(input, label)
    print(y_conv_)
    np_sum = np.sum(y_conv_)
    print(np_sum)
    print(y_conv_max_)
    index_i = 0
    for i in y_conv_:
        if y_conv_[index_i][y_conv_max_[index_i]] < 10:
            y_conv_max_[index_i] = -1
        index_i += 1
    return "{}".format(y_conv_max_)


@app.route('/update', methods=['GET'])
def update():
    model.update()
    return "success"


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 12580), app)
    server.serve_forever()
