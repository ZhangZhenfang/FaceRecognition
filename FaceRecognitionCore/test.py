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

# _, _, _, x_, y_ = data_set.read_train("E:/faces/other", 42)
# np.set_printoptions(threshold=30912)
# print(x_)

# import tensorflow as tf
# print(tf.__version__)

#!/usr/bin/python
# The contents of this file are in the public domain. See LICENSE_FOR_EXAMPLE_PROGRAMS.txt
#
#   This example program shows how to find frontal human faces in an image.  In
#   particular, it shows how you can take a list of images from the command
#   line and display each on the screen with red boxes overlaid on each human
#   face.
#
#   The examples/faces folder contains some jpg images of people.  You can run
#   this program on them and see the detections by executing the
#   following command:
#       ./face_detector.py ../examples/faces/*.jpg
#
#   This face detector is made using the now classic Histogram of Oriented
#   Gradients (HOG) feature combined with a linear classifier, an image
#   pyramid, and sliding window detection scheme.  This type of object detector
#   is fairly general and capable of detecting many types of semi-rigid objects
#   in addition to human faces.  Therefore, if you are interested in making
#   your own object detectors then read the train_object_detector.py example
#   program.
#
#
# COMPILING/INSTALLING THE DLIB PYTHON INTERFACE
#   You can install dlib using the command:
#       pip install dlib
#
#   Alternatively, if you want to compile dlib yourself then go into the dlib
#   root folder and run:
#       python setup.py install
#   or
#       python setup.py install --yes USE_AVX_INSTRUCTIONS
#   if you have a CPU that supports AVX instructions, since this makes some
#   things run faster.
#
#   Compiling dlib should work on any operating system so long as you have
#   CMake and boost-python installed.  On Ubuntu, this can be done easily by
#   running the command:
#       sudo apt-get install libboost-python-dev cmake
#
#   Also note that this example requires scikit-image which can be installed
#   via the command:
#       pip install scikit-image
#   Or downloaded from http://scikit-image.org/download.html.

# import sys
#
# import dlib
# from skimage import io
#
#
# detector = dlib.get_frontal_face_detector()
# win = dlib.image_window()
#
# for f in sys.argv[1:]:
#     print("Processing file: {}".format(f))
#     img = io.imread(f)
#     # The 1 in the second argument indicates that we should upsample the image
#     # 1 time.  This will make everything bigger and allow us to detect more
#     # faces.
#     dets = detector(img, 1)
#     print("Number of faces detected: {}".format(len(dets)))
#     for i, d in enumerate(dets):
#         print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
#             i, d.left(), d.top(), d.right(), d.bottom()))
#
#     win.clear_overlay()
#     win.set_image(img)
#     win.add_overlay(dets)
#     dlib.hit_enter_to_continue()


# Finally, if you really want to you can ask the detector to tell you the score
# for each detection.  The score is bigger for more confident detections.
# The third argument to run is an optional adjustment to the detection threshold,
# where a negative value will return more detections and a positive value fewer.
# Also, the idx tells you which of the face sub-detectors matched.  This can be
# used to broadly identify faces in different orientations.
# if (len(sys.argv[1:]) > 0):
#     img = io.imread(sys.argv[1])
#     dets, scores, idx = detector.run(img, 1, -1)
#     for i, d in enumerate(dets):
#         print("Detection {}, score: {}, face_type:{}".format(
#             d, scores[i], idx[i]))
#
# recognition_model = model.FaceRecognitionModel(
#     "E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/super_parms2.properties",
#     "E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/models", 0, 0)
# recognition_model.train("", "", 20)

# with tf.Session() as sess:
#     print(tf.__version__)
# recognition_model.update()
# for line in open("VERSION"):
#     print(line)

# f = open('VERSIONs', 'w')
# f.write('asdf\n')
# f.write('asdf\n')
# f.close()

import face_model

super_params = {
    'train_set_path':'E:/vscodeworkspace/FaceRecognition/train',
    'test_set_path':'E:/vscodeworkspace/FaceRecognition/train',
    # 'train_set_path':'C:/Users/Administrator/Desktop/facedata/train',
    # 'test_set_path':'C:/Users/Administrator/Desktop/facedata/train',
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
    'out_length': 13,
    'batch_size': 100,
    'epoch': 100
}
# new_model.train_model(super_params)
face_model.update_model(super_params, '', '', False)

