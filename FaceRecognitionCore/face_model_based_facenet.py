import tensorflow as tf
import numpy as np
import facenet
from data_set import DataSet
import os
import status_handler
image_size = 160
model_dir = './models/20170512-110547/20170512-110547.pb'


def weight_variable(shape, trainable):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial, name="w", trainable=trainable)


def bias_variable(shape, trainable):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial, name="b", trainable=trainable)


def define(out_length, keep_prob):
    tf.Graph().as_default()
    facenet.load_model(model_dir)
    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")

    # 定义全连接层1
    with tf.variable_scope("fc1"):
        fc1_length = 1024
        weights = weight_variable([128, fc1_length], True)
        biases = bias_variable([fc1_length], True)
        fc1 = tf.nn.relu(tf.matmul(embeddings, weights) + biases)
        fc1_drop = tf.nn.dropout(fc1, keep_prob)
    # 定义全连接层2
    with tf.variable_scope("fc2"):
        weights = weight_variable([1024, 512], True)
        biases = bias_variable([512], True)
        fc2 = tf.nn.relu(tf.matmul(fc1_drop, weights) + biases)
        fc2_drop = tf.nn.dropout(fc2, keep_prob)
    # 定义全连接层3
    with tf.variable_scope("fc3"):
        weights = weight_variable([512, out_length], True)
        biases = bias_variable([out_length], True)
        fc3 = tf.add(tf.matmul(fc2_drop, weights), biases, name="out")
    return fc3


def update_model(super_params, url, id, flag, model_name, start_index):
    ckpt = tf.train.get_checkpoint_state('./' + model_name + '/')
    out_length = 0
    if ckpt:
        tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')
        graph = tf.get_default_graph()
        out_length = graph.get_tensor_by_name("fc3/out:0").shape[1]
    # 每次训练重置Graph
    tf.reset_default_graph()
    log = []
    y_ = tf.placeholder(tf.float32, shape=[None, super_params['out_length']], name="y_")
    keep_prob = tf.placeholder(tf.float32, name='keep_prob')
    out = define(super_params['out_length'], keep_prob)
    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
    # 计算训练数据的正确率
    correct_prediction = tf.equal(tf.argmax(out, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')

    loss_temp = tf.losses.softmax_cross_entropy(onehot_labels=y_, logits=out)

    # 计算平均损失值
    cross_entropy_loss = tf.reduce_mean(loss_temp, name='cross_entropy_loss')
    # 反向传播调整参数
    train_step = tf.train.AdamOptimizer(learning_rate=0.001,
                                        beta1=0.9,
                                        beta2=0.999,
                                        epsilon=1e-08).minimize(cross_entropy_loss)

    saver = tf.train.Saver(max_to_keep=2)
    train_set = DataSet(super_params['train_set_path'],
                        1,
                        (super_params['input_width'], super_params['input_height'], 3),
                        super_params['batch_size'])
    test_set = DataSet(super_params['test_set_path'],
                       1,
                       (super_params['input_width'], super_params['input_height'], 3),
                       super_params['batch_size'])
    tf.add_to_collection("predict", out)
    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state('./' + model_name + '/')
        sess.run(tf.global_variables_initializer())
        if out_length != super_params['out_length']:
            loader = tf.train.Saver(
                var_list=[var for var in tf.trainable_variables() if not var.name.startswith("fc3")],
                max_to_keep=2)
        else:
            loader = tf.train.Saver(var_list=[var for var in tf.trainable_variables()],
                                    max_to_keep=2)
        print(ckpt)
        if ckpt:
            if os.path.exists(ckpt.model_checkpoint_path + '.meta'):
                print("restore")
                loader.restore(sess, ckpt.model_checkpoint_path)
                print('restored')

        for epoch in range(super_params['epoch']):
            train_set.reset()
            test_set.reset()
            step = 0
            train_loss = 0
            train_accuracy = 0
            while train_set.is_end():
                input_x, input_y, _ = train_set.next_bath()
                input_y = input_y.astype(int)
                input_y = np.eye(super_params['out_length'])[input_y]
                feed_dict = {images_placeholder: input_x,
                             y_: input_y,
                             keep_prob: super_params['keep_prob'],
                             phase_train_placeholder: False}
                train_accuracy = accuracy.eval(feed_dict=feed_dict)
                train_loss = cross_entropy_loss.eval(feed_dict=feed_dict)
                train_step.run(feed_dict=feed_dict)
                step_info = "epoch:{} step:{} loss: {:.5f} train_accuracy:{:.5f}".format(epoch,
                                                                                         step,
                                                                                         train_loss,
                                                                                         train_accuracy)
                step += 1
                print(step_info)
                log.append(step_info)
                if flag:
                    status_handler.handleTrainStep(url, id, step_info)

            if epoch % 5 == 0:
                total_accuracy = 0
                total_loss = 0
                test_step = 0
                while test_set.is_end():
                    test_x, test_y, _ = test_set.next_bath()
                    test_y = test_y.astype(int)
                    test_y = np.eye(super_params['out_length'])[test_y]
                    feed_dict = {images_placeholder: test_x,
                                 y_: test_y,
                                 keep_prob: super_params['keep_prob'],
                                 phase_train_placeholder: False}

                    test_accuracy = accuracy.eval(feed_dict=feed_dict)
                    test_loss = cross_entropy_loss.eval(feed_dict=feed_dict)
                    total_accuracy += test_accuracy
                    total_loss += test_loss
                    test_step += 1
                test_info = "TEST: epoch:{} loss: {:.5f} test_accuracy:{:.5f}".format(epoch,
                                                                                      total_loss / test_step,
                                                                                      total_accuracy / test_step)
                log.append(test_info)
                print(test_info)
                saver.save(sess, './' + model_name + '/my-model', global_step=epoch)
                if ((total_loss / test_step) < 0.001) & ((total_accuracy / test_step) > 0.99):
                    break
        saver.save(sess, './' + model_name + '/my-model', global_step=epoch)
        write_log(log, './' + model_name + '/log.txt')
    return log


def write_log(log, path):
    if os.path.exists(path):
        os.remove(path)
    fp = open(path, 'a')
    for l in log:
        fp.write(str(l) + "\n")
    fp.close()


# super_params = {
#     # 'train_set_path':'E:\\facedata\\dataset3\\train',
#     # 'test_set_path':'E:\\facedata\\dataset3\\test',
#     'train_set_path':'E:\\vscodeworkspace\\FaceRecognition\\train',
#     'test_set_path':'E:\\vscodeworkspace\\FaceRecognition\\train',
#     # 'train_set_path':'E:\\vscodeworkspace\\facedata\\data\\traindatahisted',
#     # 'test_set_path':'E:\\vscodeworkspace\\facedata\\data\\testdatahisted',
#     # 'train_set_path':'C:/Users/Administrator/Desktop/facedata/train',
#     # 'test_set_path':'C:/Users/Administrator/Desktop/facedata/train',
#     'input_height': 160,
#     'input_width': 160,
#     'input_channel': 3,
#     'conv1_filter_size': 3,
#     'conv2_filter_size': 3,
#     'conv3_filter_size': 3,
#     'conv4_filter_size': 3,
#     'conv1_filter_num': 32,
#     'conv2_filter_num': 64,
#     'conv3_filter_num': 128,
#     'conv4_filter_num': 128,
#     'fc1_length': 1024,
#     'out_length': 27,
#     'keep_prob': 1.0,
#     'batch_size': 128,
#     'epoch': 50,
#     'start_index': 1
# }
# update_model(super_params, '', '', False, 'models/facenet_based_face_model', 0)
#
