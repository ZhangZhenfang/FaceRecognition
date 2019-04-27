import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
import data_set
from font_util import FontUtil
import base64
import tensorflow as tf
monkey.patch_all()
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.sess = tf.Session()
ckpt = tf.train.get_checkpoint_state('../model2/')
saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')
print(ckpt.model_checkpoint_path)
saver.restore(app.sess, tf.train.latest_checkpoint("../model2/"))


@app.route('/')
def index():
    return 'Hello World'


@app.route('/hello')
def response_request():
    return "hi"


@app.route('/restore')
def restore():
    tf.reset_default_graph()
    app.sess = tf.Session()
    ckpt = tf.train.get_checkpoint_state('../model2/')
    saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')
    saver.restore(app.sess, ckpt.model_checkpoint_path)
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
    keep_prob = graph.get_operation_by_name("keep_prob").outputs[0]
    feed_dict = {"x:0":X, keep_prob: 1.0}
    pred_y = tf.get_collection("predict")
    pred = app.sess.run(pred_y, feed_dict)[0]
    pred_max = app.sess.run(tf.argmax(pred, 1))
    pred_soft_max = app.sess.run(tf.nn.softmax(pred))
    print("{}:{}\n{}:{}".format('max', pred, 'softmax', pred_soft_max))
    index_i = 0
    for i in pred:
        if pred_soft_max[index_i][pred_max[index_i]] < 0.9:
            pred_max[index_i] = -1
        index_i += 1
    return "{}".format(pred_max)


@app.route('/text2Mat', methods=['GET'])
def text_2_mat():
    t = request.args.get("text")
    mat = FontUtil.text2Mat(t, 15, len(t) * 12, 12)
    mat.save("./tmp.bmp")
    with open("./tmp.bmp", 'rb') as f:
        encode = base64.b64encode(f.read())
    return str(encode)


if __name__ == "__main__":

    server = pywsgi.WSGIServer(('0.0.0.0', 12580), app)
    server.serve_forever()


