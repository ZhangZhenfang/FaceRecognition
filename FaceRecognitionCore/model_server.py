import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
from font_util import FontUtil
import base64
from facenet_embeddings import Embedding
import fc_net as face_model
monkey.patch_all()
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU


app = Flask(__name__)
app.embedding = Embedding()
app.config['JSON_AS_ASCII'] = False
app.src_path = 'E:/vscodeworkspace/FaceRecognition/train'
app.npy_path = 'E:/vscodeworkspace/FaceRecognition/trainnpy'
super_params = {
    'train_set_path':'E:/vscodeworkspace/FaceRecognition/train',
    'test_set_path':'E:/vscodeworkspace/FaceRecognition/train',
    'input_height': 160,
    'input_width': 160,
    'input_channel': 3,
    'conv1_filter_size': 3,
    'conv2_filter_size': 3,
    'conv3_filter_size': 3,
    'conv4_filter_size': 3,
    'conv1_filter_num': 32,
    'conv2_filter_num': 64,
    'conv3_filter_num': 128,
    'conv4_filter_num': 128,
    'fc1_length': 1024,
    'out_length': 26,
    'keep_prob': 1.0,
    'batch_size': 128,
    'epoch': 50,
    'start_index': 1
}


@app.route('/hello')
def response_request():
    return "hi"


@app.route('/update', methods=['POST'])
def update():
    url = request.form.get('url')
    flag = False
    if url != "":
        flag = True
    print(url)
    print(flag)
    id = request.form.get('id')
    out_length = request.form.get('out_length')
    super_params['out_length'] = int(out_length)
    src_path = app.src_path
    npy_path = app.npy_path
    # if os.path.exists(npy_path):
    #
    #     # for f in os.listdir(npy_path):
    #     #     if os.path.exists(npy_path + "/" + f):
    #     #         os.remove(npy_path + "/" + f)
    # else:
    #     os.makedirs(npy_path)
    app.embedding.embedding(src_path, npy_path)
    super_params['train_set_path'] = npy_path
    super_params['test_set_path'] = npy_path
    log = face_model.update_model(super_params, url, id, flag, 'models/facenet_based_face_model_fc', 1)
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
    server = pywsgi.WSGIServer(('0.0.0.0', 12581), app)
    server.serve_forever()
