import tensorflow as tf
import data_set
import numpy as np
# import image
from PIL import Image
super_params = {
    'train_set_path':'E:\\vscodeworkspace\\facedata\data\\traindata',
    'test_set_path':'E:\\vscodeworkspace\\facedata\data\\traindata',
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
    'out_length': 7,
    'batch_size': 100,
    'epoch': 20
}

# def predict():
# images = request.files.getlist('data')
# height = int(request.form.get('height'))
# width = int(request.form.get('width'))
# channel = int(request.form.get('channel'))
ckpt = tf.train.get_checkpoint_state('../model4/')
print(ckpt)
saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')

X = data_set.read_data_set_without_label('E:\\vscodeworkspace\\facedata\\data\\testdatahisted', 128, 128, 3, 7)
graph = tf.get_default_graph()
input_x = graph.get_operation_by_name("x").outputs[0]
keep_prob = graph.get_operation_by_name("keep_prob").outputs[0]
feed_dict = {"x:0":X, keep_prob: 1.0}
pred_y = tf.get_collection("predict")
index = 0
with tf.Session() as sess:
    saver.restore(sess, ckpt.model_checkpoint_path)
    while index < X.shape[0]:
        feed_dict = {"x:0":X[index:index + 100], keep_prob: 0.8}

        pred = sess.run(pred_y, feed_dict)[0]
        pred_max = sess.run(tf.argmax(pred, 1))
        pred_soft_max = sess.run(tf.nn.softmax(pred))
        # print("{}:{}\n{}:{}".format('max', pred, 'softmax', pred_soft_max))
        index_i = 0
        for i in pred:
            if pred_soft_max[index_i][pred_max[index_i]] < 0.9:
                pred_max[index_i] = -1
            else:
                Image.fromarray(np.uint8(X[index:index + 100][index_i] * 255)).save(
                    "E:\\vscodeworkspace\\facedata\\data\\predict\\" +
                    str(pred_max[index_i]) + "\\" + str(index_i) + ".bmp")
            index_i += 1
        print(pred_max)
        index += 100
# return "{}".format(pred_max)
# predict()
