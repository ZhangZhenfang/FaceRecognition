import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
from src import model, data_set
import numpy as np
from src.font_util import FontUtil
import base64

monkey.patch_all()
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.server_model = model.FaceRecognitionModel("E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/super_parms2.properties",
                                   "E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/models",
                                              0, 0)

@app.route('/')
def index():
    return 'Hello World'


@app.route('/hello')
def response_request():
    return "hi"


@app.route('/restore')
def restore():
    del app.server_model
    app.server_model.uninstall()
    app.server_model = model.FaceRecognitionModel("E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/super_parms2.properties",
                                   "E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/models",
                                                  0, 0)
    app.server_model.restore()
    return "success"


@app.route('/predict', methods=['POST'])
def upload():
    super_parms = app.server_model.super_parms
    imgs = request.files.getlist('data')
    input_height = int(super_parms.get("input_height"))
    input_width = int(super_parms.get("input_width"))
    input_channel = int(super_parms.get("input_channel"))
    label_length = int(super_parms.get("label_length"))
    input, label = data_set.read_data(imgs, input_height, input_width, input_channel, label_length)
    y_conv_, y_conv_max_ = app.server_model.predict(input, label)
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


@app.route('/text2Mat', methods=['GET'])
def text2Mat():
    t = request.args.get("text")
    mat = FontUtil.text2Mat(t, 20, 50, 13)
    mat.save("./tmp.bmp")
    with open("./tmp.bmp", 'rb') as f:
        encode = base64.b64encode(f.read())
    return str(encode)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 12580), app)
    server.serve_forever()
