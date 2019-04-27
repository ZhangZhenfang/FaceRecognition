import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
from src.font_util import FontUtil
import base64
from src import face_model

monkey.patch_all()
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

super_params = {
    'train_set_path':'E:/vscodeworkspace/FaceRecognition/train',
    'test_set_path':'E:/vscodeworkspace/FaceRecognition/train',
    'input_height': 128,
    'input_width': 128,
    'input_channel': 3,
    'conv1_filter_size': 3,
    'conv2_filter_size': 3,
    'conv3_filter_size': 3,
    'conv1_filter_num': 32,
    'conv2_filter_num': 64,
    'conv3_filter_num': 64,
    'fc1_length': 1024,
    'out_length': 20,
    'batch_size': 100,
    'epoch': 50
}


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
    out_length = request.form.get('out_length')
    super_params['out_length'] = int(out_length)
    # version, log = model.update(url, id)
    log = face_model.update_model(super_params, url, id, True)
    return "{}={}={}={}".format("success", id, 'tmp', log)


@app.route('/text2Mat', methods=['GET'])
def text_2_mat():
    t = request.args.get("text")
    mat = FontUtil.text2Mat(t, 15, 35, 11)
    mat.save("./tmp.bmp")
    with open("./tmp.bmp", 'rb') as f:
        encode = base64.b64encode(f.read())
    return str(encode)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 12581), app)
    server.serve_forever()