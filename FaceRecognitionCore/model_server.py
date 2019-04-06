import os
from gevent import monkey
monkey.patch_all()
from flask import Flask, request
from gevent import pywsgi
import tensorflow as tf
import data_set
os.environ["CUDA_VISIBLE_DEVICES"] = "" #不使用GPU

sess = tf.Session()
meta_graph_def  = tf.saved_model.loader.load(sess, ["serve"], "E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/m1")
sig = meta_graph_def.signature_def
x = sig["test_signature"].inputs["input_x"].name
y = sig["test_signature"].inputs["input_y"].name
keep_prob = sig["test_signature"].inputs["keep_prob"].name
y_max = sig["test_signature"].outputs["y_max"].name
y_conv_max = sig["test_signature"].outputs["y_conv_max"].name

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/hello')
def response_request():
    num = request.args.get('num')
    _, _, _, x_, y_ = data_set.read_train("E:/faces/other", 42)
    y_max_, y_conv_max_ = sess.run([y_max, y_conv_max], feed_dict={x:x_, y:y_, keep_prob:1.0})
    print(y_max_)
    print(y_conv_max_)
    # for i in range (100):
    #     ret = sess.run([asquare], feed_dict={a:num})  #运行tensorflow模型
    return str(y_max_)

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 19877), app)
    server.serve_forever()
