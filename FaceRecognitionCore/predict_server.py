import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
import data_set
import numpy as np
import time
from face_model_based_facenet_and_fcnet import ModelBasedFaceNetAndFcNet

monkey.patch_all()
# os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.model = ModelBasedFaceNetAndFcNet(
    'D:/FaceRecognition/FaceRecognitionCore/models/20170512-110547/20170512-110547.pb',
    "D:/FaceRecognition/FaceRecognitionCore/models/facenet_based_face_model_fc/")


@app.route('/hello')
def response_request():
    return "hi"


@app.route('/restore', methods=['GET'])
def restore():
    app.model.load()
    return "success"


@app.route('/predict', methods=['POST'])
def predict():

    images = request.files.getlist('data')
    height = int(request.form.get('height'))
    width = int(request.form.get('width'))
    channel = int(request.form.get('channel'))
    X, Y = data_set.read_data(images, height, width, channel, 0)
    start = time.clock()
    pred, pred_soft_max, pred_max = app.model.predict(X, 1.0)
    # print("{}:{}\n{}:{}".format('max', pred, 'softmax', pred_soft_max))
    index_i = 0
    p = np.empty(len(pred_max))
    for i in pred:
        p[index_i] = pred[index_i][pred_max[index_i]]
        if pred[index_i][pred_max[index_i]] < 0.9:
            pred_max[index_i] = -1
        index_i += 1
    end = time.clock()
    print(end - start)
    return "{}, {}".format(pred_max, p)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 12580), app)
    server.serve_forever()
