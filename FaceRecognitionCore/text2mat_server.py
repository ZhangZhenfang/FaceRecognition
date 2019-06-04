import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
import data_set
from font_util import FontUtil
import base64
import numpy as np
from face_model_based_facenet_and_fcnet import ModelBasedFaceNetAndFcNet

monkey.patch_all()
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/text2Mat', methods=['GET'])
def text_2_mat():
    t = request.args.get("text")
    mat = FontUtil.text2Mat(t, 15, len(t) * 12, 12)
    mat.save("./tmp.bmp")
    with open("./tmp.bmp", 'rb') as f:
        encode = base64.b64encode(f.read())
    return str(encode)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 12587), app)
    server.serve_forever()
