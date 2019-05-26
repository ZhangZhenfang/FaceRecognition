import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
import data_set
from font_util import FontUtil
import base64
import tensorflow as tf
import numpy as np
import facenet

monkey.patch_all()
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.sess = tf.Session()
ckpt = tf.train.get_checkpoint_state('./models/model1/')
saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')
print(ckpt.model_checkpoint_path)
saver.restore(app.sess, tf.train.latest_checkpoint("./models/model1/"))


@app.route('/')
def index():
    return 'Hello World'


@app.route('/hello')
def response_request():
    return "hi"


@app.route('/restore', methods=['GET'])
def restore():
    tf.reset_default_graph()
    app.sess = tf.Session()
    ckpt = tf.train.get_checkpoint_state('./models/model1/')
    saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')
    saver.restore(app.sess, ckpt.model_checkpoint_path)
    out = tf.get_default_graph().get_tensor_by_name("fc3/out:0").shape[1]
    print('out_length: {}'.format(out))
    return "success"


# @app.route('/predict', methods=['POST'])
# def predict():
#     images = request.files.getlist('data')
#     height = int(request.form.get('height'))
#     width = int(request.form.get('width'))
#     channel = int(request.form.get('channel'))
#     X, Y = data_set.read_data(images, height, width, channel, 0)
#     graph = tf.get_default_graph()
#     input_x = graph.get_operation_by_name("x").outputs[0]
#     keep_prob = graph.get_operation_by_name("keep_prob").outputs[0]
#     feed_dict = {"x:0":X, keep_prob: 1}
#     pred_y = tf.get_collection("predict")
#     pred = app.sess.run(pred_y, feed_dict)[0]
#     pred_max = app.sess.run(tf.argmax(pred, 1))
#     pred_soft_max = app.sess.run(tf.nn.softmax(pred))
#     print("{}:{}\n{}:{}".format('max', pred, 'softmax', pred_soft_max))
#     index_i = 0
#     for i in pred:
#         if pred_soft_max[index_i][pred_max[index_i]] < 0.95:
#             pred_max[index_i] = -1
#         index_i += 1
#     return "{}".format(pred_max)

@app.route('/predict', methods=['POST'])
def predict():
    images = request.files.getlist('data')
    height = int(request.form.get('height'))
    width = int(request.form.get('width'))
    channel = int(request.form.get('channel'))
    X, Y = data_set.read_data(images, height, width, channel, 0)
    input_x = tf.get_default_graph().get_tensor_by_name("input:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
    keep_prob = tf.get_default_graph().get_operation_by_name("keep_prob").outputs[0]
    feed_dict = {input_x: X, keep_prob: 1.0, phase_train_placeholder: False}
    pred_y = tf.get_default_graph().get_tensor_by_name("fc3/out:0")
    pred = app.sess.run(pred_y, feed_dict)
    pred_soft_max = app.sess.run(tf.nn.softmax(pred))
    pred_max = app.sess.run(tf.argmax(pred_soft_max, 1))
    print("{}:{}\n{}:{}".format('max', pred, 'softmax', pred_soft_max))
    index_i = 0
    p = np.empty(len(pred_max))
    for i in pred:
        p[index_i] = pred_soft_max[index_i][pred_max[index_i]]
        if pred_soft_max[index_i][pred_max[index_i]] < 0.7:
            pred_max[index_i] = -1
        index_i += 1
    return "{}, {}".format(pred_max, p)

@app.route('/text2Mat', methods=['GET'])
def text_2_mat():
    t = request.args.get("text")
    mat = FontUtil.text2Mat(t, 15, len(t) * 10, 12)
    mat.save("./tmp.bmp")
    with open("./tmp.bmp", 'rb') as f:
        encode = base64.b64encode(f.read())
    return str(encode)


if __name__ == "__main__":

    server = pywsgi.WSGIServer(('0.0.0.0', 12580), app)
    server.serve_forever()


