import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
from src import data_set
from src.font_util import FontUtil
import base64
import tensorflow as tf

monkey.patch_all()
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

sess = tf.Session()
ckpt = tf.train.get_checkpoint_state('../model2/')
saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')
saver.restore(sess, ckpt.model_checkpoint_path)


@app.route('/')
def index():
    return 'Hello World'


@app.route('/hello')
def response_request():
    return "hi"


@app.route('/restore')
def restore():
    ckpt = tf.train.get_checkpoint_state('../model2/')
    saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')
    saver.restore(sess, ckpt.model_checkpoint_path)
    return "success"


@app.route('/predict', methods=['POST'])
def predict():
    images = request.files.getlist('data')
    height = int(request.form.get('height'))
    width = int(request.form.get('width'))
    channel = int(request.form.get('channel'))
    X, Y = data_set.read_data(images, height, width, channel, 0)
    graph = tf.get_default_graph()
    input_x = graph.get_operation_by_name("x").outputs[0]
    feed_dict = {"x:0":X}
    pred_y = tf.get_collection("predict")
    pred = sess.run(pred_y, feed_dict)[0]
    # print(pred_y)
    pred_max = sess.run(tf.argmax(pred, 1))
    print(pred)
    index_i = 0
    for i in pred:
        if pred[index_i][pred_max[index_i]] < 10:
            pred_max[index_i] = -1
        index_i += 1
    return "{}".format(pred_max)


@app.route('/text2Mat', methods=['GET'])
def text_2_mat():
    t = request.args.get("text")
    mat = FontUtil.text2Mat(t, 20, 50, 13)
    mat.save("./tmp.bmp")
    with open("./tmp.bmp", 'rb') as f:
        encode = base64.b64encode(f.read())
    return str(encode)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 12580), app)
    server.serve_forever()
