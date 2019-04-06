import os
from PIL import Image
import saver_loader_util as slutil
import tensorflow as tf
import data_set
import numpy as np
import Properties
# path = "E:/faces/s1"
# color = "E:/faces/color/source0-99/000"
#
# image_open = Image.open(path + "/10.jpg")
# colored = Image.open(color + "/000_0.bmp")
# convert = image_open.convert("RGB")
# array1 = np.array(colored)
# array2 = np.array(convert)
# array3 = np.array(image_open)
# print(image_open.mode)
# print(image_open.chanel)
# print(colored.size)
# print(array2)
# print(array3)

# parse = Properties.parse("E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/super_parms.properties")
# print(parse.get("train_path"))
# print(parse.get("test_path"))

# path = "E:/faces/other"
# image_open = Image.open(path + "/" + "s40_3.bmp")
# convert = image_open.convert("L")
# resize = image_open.resize((92, 112))
# convert.save(path + "/" + "s40_3.bmp")
# for f in os.listdir(path) :
#     image_open = Image.open(path + "/" + f)
#     resize = image_open.resize((92, 112))
#     resize.save(path + "/_" + f)
    # convert = image_open.convert("L")
    # convert.save(path + "/" + f)



# with tf.Session() as sess:
#     load = tf.saved_model.loader.load(sess, ["test1"], "./m1")
#     # slutil.loader1(tf, "./m1", sess, )
#     print(sess.graph.get_operations())
#     x_ = sess.graph.get_tensor_by_name("x:0")
#     y_ = sess.graph.get_tensor_by_name("y_:0")
#     y_max_ = sess.graph.get_tensor_by_name("y_max:0")
#     y_conv_max_ = sess.graph.get_tensor_by_name("y_conv_max:0")
#     keep_prob = sess.graph.get_tensor_by_name("keep_prob:0")
#     _, _, _, test, test_labels = data_set.read_train("E:/faces/other", 42)
#     y_max_, y_conv_max_ = sess.run([y_max_, y_conv_max_], feed_dict={x_: test, y_:test_labels, keep_prob: 1.0})
#     print(y_max_)
#     print(y_conv_max_)

# import urllib.parse
# import http.client
# test_data = {'x':'[1]','y_':'[1]'}
#
# test_data_urlencode = urllib.parse.urlencode(test_data)
#
# requrl = "http://47.107.48.115:8051/v1/models/m1"
# headerdata = {"Host":"47.107.48.115"}
#
# conn = http.client.HTTPConnection("47.107.48.115")
#
# conn.request(method="POST", url=requrl, body=test_data_urlencode, headers = headerdata)
#
# response = conn.getresponse()
#
# res= response.read()
#
# print(res)

# with tf.Session() as sess :
#     meta_graph_def  = tf.saved_model.loader.load(sess, ["serve"], "E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/m1")
#     sig = meta_graph_def.signature_def
#     x = sig["test_signature"].inputs["input_x"].name
#     y = sig["test_signature"].inputs["input_y"].name
#     keep_prob = sig["test_signature"].inputs["keep_prob"].name
#     y_max = sig["test_signature"].outputs["y_max"].name
#     y_conv_max = sig["test_signature"].outputs["y_conv_max"].name
#     _, _, _, x_, y_ = data_set.read_train("E:/faces/other", 42)
#     y_max_, y_conv_max_ = sess.run([y_max, y_conv_max], feed_dict={x:x_, y:y_, keep_prob:1.0})
#     print(y_max_)
#     print(y_conv_max_)

import json
# _, _, _, x_, y_ = data_set.read_train("E:/faces/other", 42)
# np.set_printoptions(threshold=30912)
# print(x_)

# import tensorflow as tf
# print(tf.__version__)

with tf.Session() as sess:
    meta_graph_def = tf.saved_model.loader.load(sess,
                                                ["serve"],
                                                "E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/m1")
    sig = meta_graph_def.signature_def
    x = sig["test_signature"].inputs["input_x"].name
    y = sig["test_signature"].inputs["input_y"].name
    keep_prob = sig["test_signature"].inputs["keep_prob"].name
    y_max = sig["test_signature"].outputs["y_max"].name
    y_conv = sig["test_signature"].outputs["y_conv"].name
    y_conv_max = sig["test_signature"].outputs["y_conv_max"].name

    x_, y_ = data_set.read_data_set("E:/faces/other",
                                    112,
                                    92,
                                    3,
                                    42)

    y_conv, y_max_, y_conv_max_ = sess.run([y_conv, y_max, y_conv_max],
                                           feed_dict={x: x_, y: y_, keep_prob: 1.0})
    print(y_conv)
    print(y_max_)
    print(y_conv_max_)
