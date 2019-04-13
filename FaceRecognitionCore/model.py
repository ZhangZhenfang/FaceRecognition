import data_set
import tensorflow as tf
import numpy as np
import properties
import math
import os
import status_handler

class FaceRecognitionModel:

    def __init__(self, propertityPath, save_path, batch_size, label_length):
        self.save_path = save_path
        self.super_parms = properties.parse(propertityPath)
        self.input_height = int(self.super_parms.get("input_height"))
        self.input_width = int(self.super_parms.get("input_width"))
        self.input_channel = int(self.super_parms.get("input_channel"))
        self.steps = []
        f = open('VERSION')
        self.current_version = int(f.readline())
        # self.save_path = '{}{}{}'.format(save_path, '/', current_version)
        label_length_ = int(f.readline())
        if label_length != 0:
            self.label_length = label_length
        else:
            self.label_length = label_length_
        if batch_size != 0:
            self.batch_size = batch_size
        else:
            self.batch_size = int(self.super_parms.get("batch_size"))
        conv1_filters = int(self.super_parms.get("conv1_filters"))
        conv2_filters = int(self.super_parms.get("conv2_filters"))
        conv3_filters = int(self.super_parms.get("conv3_filters"))
        conv1_filter_size = int(self.super_parms.get("conv1_filter_size"))
        conv2_filter_size = int(self.super_parms.get("conv2_filter_size"))
        conv3_filter_size = int(self.super_parms.get("conv3_filter_size"))
        learn_rate = float(self.super_parms.get("learn_rate"))

        # 定义输入数据
        self.x = tf.placeholder(tf.float32, shape=[None, self.input_height, self.input_width,
                                                   self.input_channel], name="x")
        # 定义输出数据
        self.y = tf.placeholder(tf.float32, shape=[None, self.label_length], name="y")

        # x_image = tf.reshape(x, [-1, height, width, 3])
        self.keep_prob = tf.placeholder(tf.float32, name="keep_prob")
        # 卷积层1卷积核
        W_conv1 = tf.Variable(tf.truncated_normal([conv1_filter_size, conv1_filter_size, self.input_channel,
                                                   conv1_filters], stddev=0.1))
        # 卷积层1偏置
        b_conv1 = tf.constant(0.1, shape=[conv1_filters])

        # 卷积层1卷积后经过激活函数relu的结果
        h_conv1 = tf.nn.relu(tf.nn.conv2d(self.x, W_conv1, strides=[1, 1, 1, 1], padding='SAME') + b_conv1)
        # 进行卷积层1的池化操作
        h_pool1 = tf.nn.max_pool(h_conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # h_pool1 = tf.nn.dropout(h_pool1, keep_prob)
        # 卷积层2卷积核
        W_conv2 = tf.Variable(tf.truncated_normal([conv2_filter_size, conv2_filter_size, conv1_filters, conv2_filters],
                                                  stddev=0.1))
        # 卷积层2偏置
        b_conv2 = tf.constant(0.1, shape=[conv2_filters])

        # 卷积层2卷积后经过relu激活函数的结果
        h_conv2 = tf.nn.relu(tf.nn.conv2d(h_pool1, W_conv2, strides=[1, 1, 1, 1], padding='SAME') + b_conv2)
        # 进行卷积层2池化操作
        h_pool2 = tf.nn.max_pool(h_conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        # h_pool2 = tf.nn.dropout(h_pool2, keep_prob)

        W_conv3 = tf.Variable(tf.truncated_normal([conv3_filter_size, conv3_filter_size, conv2_filters, conv3_filters],
                                                  stddev=0.1))
        b_conv3 = tf.constant(0.1, shape=[conv3_filters])

        h_conv3 = tf.nn.relu(tf.nn.conv2d(h_pool2, W_conv3, strides=[1, 1, 1, 1], padding='SAME') + b_conv3)
        h_pool3 = tf.nn.max_pool(h_conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        h_pool3 = tf.nn.dropout(h_pool3, self.keep_prob)
        # 全连接层1权重定义
        W_fc1 = tf.Variable(tf.truncated_normal([math.ceil(self.input_height / 8) * math.ceil(self.input_width / 8)
                                                 * conv3_filters, 1024], stddev=0.1))
        # 全连接层1偏置定义
        b_fc1 = tf.constant(0.1, shape=[1024])

        # 对卷积层2的输出展开
        h_pool3 = tf.reshape(h_pool3, [-1, math.ceil(self.input_height / 8)
                                       * math.ceil(self.input_width / 8)
                                       * conv3_filters])
        # 全连接层1，上一层的输出矩阵乘权重后加偏置后经过激活函数
        h_fc1 = tf.nn.relu(tf.matmul(h_pool3, W_fc1) + b_fc1)

        # dropout可解决过拟合问题

        h_fc1 = tf.nn.dropout(h_fc1, self.keep_prob)

        # 全连接层2权重
        W_fc2 = tf.Variable(tf.truncated_normal([1024, self.label_length], stddev=0.1))
        # 全连接层2偏置
        b_fc2 = tf.constant(0.1, shape=[self.label_length])

        # 输出
        self.y_conv = tf.matmul(h_fc1, W_fc2) + b_fc2

        # 交叉熵
        cross_entry = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.y, logits=self.y_conv))
        # 选择优化器对交叉熵进行最小化优化
        self.train_step = tf.train.AdamOptimizer(learn_rate).minimize(cross_entry, name="train_step")

        # 计算正确的个数，向量对应的位置的数进行比较，相等则对应位置为True
        self.y_max = tf.argmax(self.y, 1, name="y_max")
        self.y_conv_max = tf.argmax(self.y_conv, 1, name="y_conv_max")
        # 预测值
        prediction = tf.argmax(self.y_conv, 1)
        correct_prediction = tf.equal(self.y_max, self.y_conv_max)
        # 计算训练准确率，将True转为1，然后计算平均值
        self.train_accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="train_accuracy")

        inputs = {
                    'input_x': tf.saved_model.utils.build_tensor_info(self.x),
                    'input_y': tf.saved_model.utils.build_tensor_info(self.y),
                    'keep_prob': tf.saved_model.utils.build_tensor_info(self.keep_prob)
                }

        # y 为最终需要的输出结果tensor
        outputs = {
                    'y_max': tf.saved_model.utils.build_tensor_info(self.y_max),
                    'y_conv': tf.saved_model.utils.build_tensor_info(self.y_conv),
                    'y_conv_max': tf.saved_model.utils.build_tensor_info(self.y_conv_max),
                    # 'train_step': tf.saved_model.utils.build_tensor_info(self.train_step.),
                    'train_accuracy': tf.saved_model.utils.build_tensor_info(self.train_accuracy),
        }
        self.saver = tf.train.Saver()
        self.loaded = False
        self.sess = tf.Session()

    def train(self, url, id):
        self.steps.clear()
        f = open('VERSION', 'r')
        last_version = f.readline()
        print(last_version)
        last_version = int(last_version)
        f.close()
        train, train_labels = data_set.read_data_set(self.super_parms.get("train_path"),
                                                     self.input_height,
                                                     self.input_width,
                                                     self.input_channel,
                                                     self.label_length)
        test, test_labels = data_set.read_data_set(self.super_parms.get("test_path"),
                                                   self.input_height,
                                                   self.input_width,
                                                   self.input_channel,
                                                   self.label_length)
        epoch = train.shape[0]
        batch_size = self.batch_size
        times = epoch / batch_size
        threshold = 0.98
        print(epoch)

        # with tf.Session() as sess:
        self.sess.run(tf.global_variables_initializer())
        index = 0
        epoch_index = 1
        for i in range(200):
            if index + batch_size >= epoch:
                input_x = train[index: epoch]
                input_y = train_labels[index: epoch]
                index = 0
                epoch_index += 1
                l = list(zip(train, train_labels))
                np.random.shuffle(l)
                train, train_labels = zip(*l)
            else:
                input_x = train[index:index + batch_size]
                input_y = train_labels[index:index + batch_size]
                index += batch_size
            _, accuracy = self.sess.run([self.train_step, self.train_accuracy],
            feed_dict={self.x: input_x, self.y: input_y, self.keep_prob: 0.5})
            # saver.save(sess, './mnist_model/model.ckpt')

            l = list(zip(test, test_labels))
            np.random.shuffle(l)
            test, test_labels = zip(*l)
            y_max_, y_conv_max_, test_accuracy_ = self.sess.run([self.y_max,
                                                             self.y_conv_max,
                                                             self.train_accuracy],
                                                            feed_dict={self.x: test,
                                                                       self.y: test_labels,
                                                                       self.keep_prob: 1.0})
            step_status = "epoch:{} batch:{} train_accuracy:{:.3f} test_accuracy:{:.3f}".format(epoch_index,
                                                                                        i,
                                                                                        accuracy,
                                                                                        test_accuracy_)
            self.steps.append(step_status)
            print(step_status)
            status_handler.handleTrainStep(url, id, step_status)

            if (accuracy >= threshold) & (test_accuracy_ >= threshold) & (i > 50):

                break
        current_version = str(last_version + 1)
        self.saver.save(self.sess, self.save_path + '/' + current_version + '/model.ckpt')
        f = open('VERSION', 'w')
        f.write(current_version + '\n')
        f.write(str(self.label_length) + '\n')
        f.write(self.save_path + '/' + current_version + '/model.ckpt\n')
        for s in self.steps:
            f.write(s + '\n')
        f.close()
        return current_version, self.steps

    def predict(self, input, label):
        if self.loaded == False:
            self.loaded = True
            v = str(self.current_version)
            self.saver.restore(self.sess, self.save_path + '/' + v + "/model.ckpt")
        y_conv_, y_conv_max_ = self.sess.run([self.y_conv, self.y_conv_max], feed_dict={self.x: input,
                                                                                       self.y: label,
                                                                                       self.keep_prob: 1.0})
        return y_conv_, y_conv_max_

    def update(self, url, id):
        self.steps.clear()
        f = open('VERSION', 'r')
        last_version = f.readline()
        f.readline()
        last_path = f.readline()
        last_path = last_path.replace('\n', '')
        last_version = int(last_version)
        current_version = last_version + 1
        current_version = str(current_version)
        f.close()
        train, train_labels = data_set.read_data_set(self.super_parms.get("train_path"),
                                                     self.input_height,
                                                     self.input_width,
                                                     self.input_channel,
                                                     self.label_length)
        test, test_labels = data_set.read_data_set(self.super_parms.get("test_path"),
                                                   self.input_height,
                                                   self.input_width,
                                                   self.input_channel,
                                                   self.label_length)

        epoch = train.shape[0]
        batch_size = 6
        times = epoch / batch_size
        threshold = 0.98
        print(epoch)
        l = list(zip(train, train_labels))
        np.random.shuffle(l)
        train, train_labels = zip(*l)
        if self.loaded == False: # 如果未加载则加载参数或者重新初始化参数
            self.loaded = True
            # print(last_path + '.index')
            if os.path.exists(last_path + '.index'): # 存在则restore
                print('restore')
                self.saver.restore(self.sess, last_path)
            else: # 不存在则重新初始化参数
                print('init')
                self.sess.run(tf.global_variables_initializer())
        index = 0
        epoch_index = 1
        for i in range(100):
            if index + batch_size >= epoch:
                input_x = train[index: epoch]
                input_y = train_labels[index: epoch]
                index = 0
                epoch_index += 1
                l = list(zip(train, train_labels))
                np.random.shuffle(l)
                train, train_labels = zip(*l)
            else:
                input_x = train[index:index + batch_size]
                input_y = train_labels[index:index + batch_size]
                index += batch_size
            _, accuracy = self.sess.run([self.train_step, self.train_accuracy],
            feed_dict={self.x: input_x, self.y: input_y, self.keep_prob: 0.5})

            l = list(zip(test, test_labels))
            np.random.shuffle(l)
            test, test_labels = zip(*l)
            y_max_, y_conv_max_, test_accuracy_ = self.sess.run([self.y_max,
                                                             self.y_conv_max,
                                                             self.train_accuracy],
                                                            feed_dict={self.x: test,
                                                                       self.y: test_labels,
                                                                       self.keep_prob: 1.0})
            step_status = "epoch:{} batch:{} train_accuracy:{:.3f} test_accuracy:{:.3f}".format(epoch_index,
                                                                                        i,
                                                                                        accuracy,
                                                                                        test_accuracy_)
            self.steps.append(step_status)
            print(step_status)
            status_handler.handleTrainStep(url, id, step_status)
            if (accuracy >= threshold) & (test_accuracy_ >= threshold) & (i > 20):
                break
        print(self.save_path + '/' + current_version + '/model.ckpt')
        self.saver.save(self.sess, self.save_path + '/' + current_version + '/model.ckpt')
        f = open('VERSION', 'w')
        f.write(current_version + '\n')
        f.write(str(self.label_length) + '\n')
        f.write(self.save_path + '/' + current_version + '/model.ckpt\n')
        for s in self.steps:
            f.write(s + '\n')
        f.close()
        return current_version, self.steps

