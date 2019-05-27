import tensorflow as tf
import status_handler
import math
import numpy as np
import os
from data_set import DataSet


def define_model(x, super_params, keep_prob):
    def weight_variable(shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial, name="w")

    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial, name="b")

    def conv2d(x, W):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2d(x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    conv_out_height = super_params['input_height']
    conv_out_width = super_params['input_width']

    # 定义卷积层1
    with tf.variable_scope("conv1"):
        conv_out_height = math.ceil(conv_out_height / 2)
        conv_out_width = math.ceil(conv_out_width / 2)
        size = super_params['conv1_filter_size']
        num = super_params['conv1_filter_num']
        input_channel = super_params['input_channel']
        weights1_1 = weight_variable([size, size, input_channel, num])
        biases1_1 = bias_variable([num])
        conv1_1 = tf.nn.relu(conv2d(x, weights1_1) + biases1_1)

        # input_channel = num
        # weights1_2 = weight_variable([size, size, input_channel, num])
        # biases1_2 = bias_variable([num])
        # conv1_2 = tf.nn.relu(conv2d(conv1_1, weights1_2) + biases1_2)
        pool1 = max_pool_2d(conv1_1)
    # 定义卷积层2
    with tf.variable_scope("conv2"):
        conv_out_height = math.ceil(conv_out_height / 2)
        conv_out_width = math.ceil(conv_out_width / 2)
        size = super_params['conv2_filter_size']
        num = super_params['conv2_filter_num']
        input_channel = super_params['conv1_filter_num']
        weights2_1 = weight_variable([size, size, input_channel, num])
        biases2_1 = bias_variable([num])
        conv2_1 = tf.nn.relu(conv2d(pool1, weights2_1) + biases2_1)

        # input_channel = num
        # weights2_2 = weight_variable([size, size, input_channel, num])
        # biases2_2 = bias_variable([num])
        # conv2_2 = tf.nn.relu(conv2d(conv2_1, weights2_2) + biases2_2)
        pool2 = max_pool_2d(conv2_1)
    # 定义卷积层3
    with tf.variable_scope("conv3"):
        conv_out_height = math.ceil(conv_out_height / 2)
        conv_out_width = math.ceil(conv_out_width / 2)
        size = super_params['conv3_filter_size']
        num = super_params['conv3_filter_num']
        input_channel = super_params['conv2_filter_num']
        weights3_1 = weight_variable([size, size, input_channel, num])
        biases3_1 = bias_variable([num])
        conv3_1 = tf.nn.relu(conv2d(pool2, weights3_1) + biases3_1)

        # input_channel = num
        # weights3_2 = weight_variable([size, size, input_channel, num])
        # biases3_2 = bias_variable([num])
        # conv3_2 = tf.nn.relu(conv2d(conv3_1, weights3_2) + biases3_2)
        pool3 = max_pool_2d(conv3_1)
    # 定义卷积层4
    # with tf.variable_scope("conv4"):
    #     conv_out_height = math.ceil(conv_out_height / 2)
    #     conv_out_width = math.ceil(conv_out_width / 2)
    #     size = super_params['conv4_filter_size']
    #     num = super_params['conv4_filter_num']
    #     input_channel = super_params['conv3_filter_num']
    #     weights4_1 = weight_variable([size, size, input_channel, num])
    #     biases4_1 = bias_variable([num])
    #     conv4_1 = tf.nn.relu(conv2d(pool3, weights4_1) + biases4_1)

        # input_channel = super_params['conv3_filter_num']
        # weights4_2 = weight_variable([size, size, input_channel, num])
        # biases4_2 = bias_variable([num])
        # conv4_2 = tf.nn.relu(conv2d(conv4_1, weights4_2) + biases4_2)

        # pool4 = max_pool_2d(conv4_1)
    # 定义全连接层1
    with tf.variable_scope("fc1"):
        fc1_length = super_params['fc1_length']
        input_channel = super_params['conv3_filter_num']
        weights = weight_variable([conv_out_height * conv_out_width * input_channel, fc1_length]) # [-1,1024]
        biases = bias_variable([fc1_length])
        fc1_flat = tf.reshape(pool3, [-1, conv_out_height * conv_out_width * input_channel])
        fc1 = tf.nn.relu(tf.matmul(fc1_flat, weights) + biases)
        fc1_drop = tf.nn.dropout(fc1, keep_prob)
    # 定义全连接层1
    with tf.variable_scope("fc2"):
        fc1_length = super_params['fc1_length']
        out_length = super_params['out_length']
        weights = weight_variable([fc1_length, out_length])
        biases = bias_variable([out_length])
        fc2 = tf.add(tf.matmul(fc1_drop, weights), biases, name="out")
    return fc2


def update_model(super_params, url, id, flag, model_name, start_index):
    ckpt = tf.train.get_checkpoint_state('./' + model_name + '/')
    out = 0
    if ckpt:
        tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')
        graph = tf.get_default_graph()
        out = graph.get_tensor_by_name("fc2/out:0").shape[1]
    # 每次训练重置Graph
    tf.reset_default_graph()

    log = []
    input_height = super_params['input_height']
    input_width = super_params['input_width']
    input_chaneel = super_params['input_channel']
    # 输入数据X，将作为模型的输入数据
    x = tf.placeholder(tf.float32, shape=[None, input_height, input_width, input_chaneel], name="x")
    # 输入数据Y
    y_ = tf.placeholder(tf.float32, shape=[None, super_params['out_length']], name="y_")
    keep_prob = tf.placeholder(tf.float32, name='keep_prob')
    initial_learning_rate = 0.0001
    # 定义模型结构并且获取输出层
    y_fc2 = define_model(x, super_params, keep_prob)
    # 定义损失函数
    loss_temp = tf.losses.softmax_cross_entropy(onehot_labels=y_, logits=y_fc2)
    # 计算平均损失值
    cross_entropy_loss = tf.reduce_mean(loss_temp, name='cross_entropy_loss')
    # 反向传播调整参数
    train_step = tf.train.AdamOptimizer(learning_rate=initial_learning_rate, beta1=0.9, beta2=0.999,
                                        epsilon=1e-08).minimize(cross_entropy_loss)
    # 计算训练数据的正确率
    correct_prediction = tf.equal(tf.argmax(y_fc2, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')

    tf.add_to_collection("predict", y_fc2)

    train_set = DataSet(super_params['train_set_path'], super_params['start_index'], (128, 128, 3), super_params['batch_size'])
    test_set = DataSet(super_params['test_set_path'], super_params['start_index'], (128, 128, 3), super_params['batch_size'])
    with tf.Session() as sess:
        writer = tf.summary.FileWriter('logs', sess.graph) #将训练日志写入到logs文件夹下
        train_accuracy_scalar = tf.summary.scalar('train_accuracy', accuracy)
        train_loss_scalar = tf.summary.scalar('train_loss', cross_entropy_loss)

        ckpt = tf.train.get_checkpoint_state('./' + model_name + '/')
        sess.run(tf.global_variables_initializer())
        if out != super_params['out_length']:
            loader = tf.train.Saver(var_list=[var for var in tf.trainable_variables() if not var.name.startswith("fc2")],
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
        print('traindata loaded')

        saver = tf.train.Saver(max_to_keep=2)

        for epoch in range(super_params['epoch']):
            train_set.reset()
            test_set.reset()
            step = 0
            train_loss = 0
            train_accuracy = 0
            while train_set.is_end():
                input_x, input_y = train_set.next_bath()
                input_y = input_y.astype(int)
                input_y = np.eye(super_params['out_length'])[input_y]
                feed_dict = {x: input_x,
                             y_: input_y,
                             keep_prob: super_params['keep_prob']}
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
                accuracy_scalar, loss_scalar = sess.run([train_accuracy_scalar, train_loss_scalar],
                                                    feed_dict={x: input_x, y_: input_y, keep_prob: 0.5})
                writer.add_summary(accuracy_scalar, epoch)
                writer.add_summary(loss_scalar, epoch)

            if epoch % 5 == 0:
                total_accuracy = 0
                total_loss = 0
                test_step = 0
                while test_set.is_end():
                    test_x, test_y = test_set.next_bath()
                    test_y = test_y.astype(int)
                    test_y = np.eye(super_params['out_length'])[test_y]
                    feed_dict = {x: test_x,
                                 y_: test_y,
                                 keep_prob: super_params['keep_prob']}

                    test_accuracy = accuracy.eval(feed_dict=feed_dict)
                    test_loss = cross_entropy_loss.eval(feed_dict=feed_dict)
                    total_accuracy += test_accuracy
                    total_loss += test_loss
                    test_step += 1
                test_info = "TEST: epoch:{} loss: {:.5f} test_accuracy:{:.5f}".format(epoch,
                                                                                      (total_loss / test_step),
                                                                                      (total_accuracy / test_step))
                log.append(test_info)
                print(test_info)
                saver.save(sess, './' + model_name + '/my-model', global_step=epoch)
                if ((total_loss / test_step) > 0.99) & ((total_accuracy / test_step) < 0.1):
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


super_params = {
    'train_set_path':'E:\\facedata\\dataset3\\train',
    'test_set_path':'E:\\facedata\\dataset3\\test',
    # 'train_set_path':'E:\\vscodeworkspace\\FaceRecognition\\train',
    # 'test_set_path':'E:\\vscodeworkspace\\FaceRecognition\\train',
    # 'train_set_path':'E:\\vscodeworkspace\\facedata\\data\\traindatahisted',
    # 'test_set_path':'E:\\vscodeworkspace\\facedata\\data\\testdatahisted',
    # 'train_set_path':'C:/Users/Administrator/Desktop/facedata/train',
    # 'test_set_path':'C:/Users/Administrator/Desktop/facedata/train',
    'input_height': 128,
    'input_width': 128,
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
    'out_length': 25,
    'keep_prob': 0.5,
    'batch_size': 128,
    'epoch': 200,
    'start_index': 1
}

update_model(super_params, '', '', False, 'models/weibo_model', 0)
