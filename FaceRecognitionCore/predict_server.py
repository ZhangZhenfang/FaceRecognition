import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
import data_set
import numpy as np
from face_model_based_facenet_and_fcnet import ModelBasedFaceNetAndFcNet

monkey.patch_all()
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.model = ModelBasedFaceNetAndFcNet('./models/20170512-110547/20170512-110547.pb', "./models/facenet_based_face_model_fc/")


@app.route('/hello')
def response_request():
    return "hi"


@app.route('/restore', methods=['GET'])
def restore():
    app.model.load()
    return "success"


@app.route('/predict', methods=['POST'])
def predict():
    print('12585')
    images = request.files.getlist('data')
    height = int(request.form.get('height'))
    width = int(request.form.get('width'))
    channel = int(request.form.get('channel'))
    X, Y = data_set.read_data(images, height, width, channel, 0)
    pred = app.model.predict(X, 1.0)
    pred_soft_max = app.model.sess.run(app.model.tf.nn.softmax(pred))
    pred_max = app.model.sess.run(app.model.tf.argmax(pred_soft_max, 1))
    print("{}:{}\n{}:{}".format('max', pred, 'softmax', pred_soft_max))
    index_i = 0
    p = np.empty(len(pred_max))
    for i in pred:
        p[index_i] = pred_soft_max[index_i][pred_max[index_i]]
        if pred_soft_max[index_i][pred_max[index_i]] < 0.9:
            pred_max[index_i] = -1
        index_i += 1
    return "{}, {}".format(pred_max, p)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 12580), app)
    server.serve_forever()
