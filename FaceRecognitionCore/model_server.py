import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
import model


monkey.patch_all()
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU

model = model.FaceRecognitionModel("E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/super_parms2.properties",
                                   "E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/models", 0, 0)
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    return 'Hello World'


@app.route('/hello')
def response_request():
    return "hi"


@app.route('/update', methods=['POST'])
def update():
    url = request.form.get('url')
    id = request.form.get('id')
    print(id)
    print(url)
    version, log = model.update(url, id)
    return "{}={}={}={}".format("success", id, version, log)


@app.route('/train', methods=['POST'])
def train():
    batch_size = request.form.get('batch_size')
    label_length = request.form.get('label_length')
    model.label_length = label_length
    model.batch_size = batch_size
    print(model.label_length)
    print(model.batch_size)
    # model.train()
    return "success"


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 12581), app)
    server.serve_forever()
