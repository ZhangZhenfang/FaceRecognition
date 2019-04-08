import os
from gevent import monkey
from flask import Flask, request
from gevent import pywsgi
import tensorflow as tf
import data_set
import properties

monkey.patch_all()
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU

sess = tf.Session()
meta_graph_def = tf.saved_model.loader.load(sess,
                                            ["serve"],
                                            "E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/m3")
sig = meta_graph_def.signature_def
x = sig["test_signature"].inputs["input_x"].name
y = sig["test_signature"].inputs["input_y"].name
keep_prob = sig["test_signature"].inputs["keep_prob"].name
y_max = sig["test_signature"].outputs["y_max"].name
y_conv = sig["test_signature"].outputs["y_conv"].name
y_conv_max = sig["test_signature"].outputs["y_conv_max"].name

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/hello')
def response_request():
    x_, y_ = data_set.read_data_set("E:/faces/other", 112, 92, 3, 42)
    y_conv_, y_max_, y_conv_max_ = sess.run([y_conv, y_max, y_conv_max], feed_dict={x:x_, y:y_, keep_prob:1.0})
    print(y_max_)
    print(y_conv_max_)
    return str(y_conv_max_)
@app.route('/upload', methods=['POST'])
def upload():
    super_parms = properties.parse("E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/super_parms2.properties")
    imgs = request.files.getlist('data')
    input_height = int(super_parms.get("input_height"))
    input_width = int(super_parms.get("input_width"))
    input_channel = int(super_parms.get("input_channel"))
    label_length = int(super_parms.get("label_length"))
    input, label = data_set.read_data(imgs, input_height, input_width, input_channel, label_length)
    y_conv_, y_conv_max_ = sess.run([y_conv, y_conv_max], feed_dict={x: input, y: label, keep_prob: 1.0})
    # print(y_conv_)
    # print(y_conv_max_)
    index_i = 0
    for i in y_conv_:
        if y_conv_[index_i][y_conv_max_[index_i]] < 10:
            y_conv_max_[index_i] = -1
        index_i += 1
    return ("{}".format(y_conv_max_))

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 12580), app)
    server.serve_forever()
