import tensorflow as tf
from src import data_set, status_handler
import math
import numpy as np
import os


def define_model(x, super_params):
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

    with tf.variable_scope("conv1"):  # [-1,32,32,3]
        conv_out_height = math.ceil(conv_out_height / 2)
        conv_out_width = math.ceil(conv_out_width / 2)
        size = super_params['conv1_filter_size']
        num = super_params['conv1_filter_num']
        input_channel = super_params['input_channel']
        weights = weight_variable([size, size, input_channel, num])
        biases = bias_variable([num])
        conv1 = tf.nn.relu(conv2d(x, weights) + biases)
        pool1 = max_pool_2d(conv1)  # [-1,11,11,32]

    with tf.variable_scope("conv2"):
        conv_out_height = math.ceil(conv_out_height / 2)
        conv_out_width = math.ceil(conv_out_width / 2)
        size = super_params['conv2_filter_size']
        num = super_params['conv2_filter_num']
        input_channel = super_params['conv1_filter_num']
        weights = weight_variable([size, size, input_channel, num])
        biases = bias_variable([num])
        conv2 = tf.nn.relu(conv2d(pool1, weights) + biases)
        pool2 = max_pool_2d(conv2) # [-1,4,4,64]

    with tf.variable_scope("conv3"):
        conv_out_height = math.ceil(conv_out_height / 2)
        conv_out_width = math.ceil(conv_out_width / 2)
        size = super_params['conv3_filter_size']
        num = super_params['conv3_filter_num']
        input_channel = super_params['conv2_filter_num']
        weights = weight_variable([size, size, input_channel, num])
        biases = bias_variable([num])
        conv3 = tf.nn.relu(conv2d(pool2, weights) + biases)
        pool3 = max_pool_2d(conv3) # [-1,4,4,64]

    with tf.variable_scope("fc1"):
        fc1_length = super_params['fc1_length']
        input_channel = super_params['conv3_filter_num']
        weights = weight_variable([conv_out_height * conv_out_width * input_channel, fc1_length]) # [-1,1024]
        biases = bias_variable([fc1_length])
        fc1_flat = tf.reshape(pool3, [-1, conv_out_height * conv_out_width * input_channel])
        fc1 = tf.nn.relu(tf.matmul(fc1_flat, weights) + biases)
        fc1_drop = tf.nn.dropout(fc1, 0.5) # [-1,128]

    with tf.variable_scope("fc2"):
        fc1_length = super_params['fc1_length']
        out_length = super_params['out_length']
        weights = weight_variable([fc1_length, out_length])
        biases = bias_variable([out_length])
        fc2 = tf.matmul(fc1_drop, weights) + biases # [-1,4]
    return fc2


def train_model(super_params):
    input_height = super_params['input_height']
    input_width = super_params['input_width']
    input_chaneel = super_params['input_chaneel']
    x = tf.placeholder(tf.float32, shape=[None, input_height, input_width, input_chaneel], name="x")
    y_ = tf.placeholder(tf.float32, shape=[None, super_params['out_length']], name="y_")

    initial_learning_rate = 0.001
    y_fc2 = define_model(x, super_params)

    loss_temp = tf.losses.softmax_cross_entropy(onehot_labels=y_, logits=y_fc2)
    cross_entropy_loss = tf.reduce_mean(loss_temp, name='cross_entropy_loss')

    train_step = tf.train.AdamOptimizer(learning_rate=initial_learning_rate, beta1=0.9, beta2=0.999,
                                        epsilon=1e-08).minimize(cross_entropy_loss)

    correct_prediction = tf.equal(tf.argmax(y_fc2, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')

    # save model
    saver = tf.train.Saver(max_to_keep=4)
    tf.add_to_collection("predict", y_fc2)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print("------------------------------------------------------")
        X, Y = data_set.read_data_set('E:/vscodeworkspace/FaceRecognition/train', 128, 128, 3, super_params['out_length'])
        for epoch in range(200):
            if epoch % 10 == 0:
                print("------------------------------------------------------")

                train_accuracy = accuracy.eval(feed_dict={x: X, y_: Y})
                train_loss = cross_entropy_loss.eval(feed_dict={x: X, y_: Y})

                print("after epoch %d, the loss is %6f" % (epoch, train_loss))
                print("after epoch %d, the acc is %6f" % (epoch, train_accuracy))

                saver.save(sess, "model2/my-model", global_step=epoch)
                print("save the model")

            train_step.run(feed_dict={x: X, y_: Y})

        print("------------------------------------------------------")


def update_model(super_params, url, id):
    log = []
    input_height = super_params['input_height']
    input_width = super_params['input_width']
    input_chaneel = super_params['input_channel']
    x = tf.placeholder(tf.float32, shape=[None, input_height, input_width, input_chaneel], name="x")
    y_ = tf.placeholder(tf.float32, shape=[None, super_params['out_length']], name="y_")

    initial_learning_rate = 0.001
    y_fc2 = define_model(x, super_params)

    loss_temp = tf.losses.softmax_cross_entropy(onehot_labels=y_, logits=y_fc2)
    cross_entropy_loss = tf.reduce_mean(loss_temp, name='cross_entropy_loss')

    train_step = tf.train.AdamOptimizer(learning_rate=initial_learning_rate, beta1=0.9, beta2=0.999,
                                        epsilon=1e-08).minimize(cross_entropy_loss)

    correct_prediction = tf.equal(tf.argmax(y_fc2, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')

    # save model
    # saver = tf.train.Saver(max_to_keep=4)
    tf.add_to_collection("predict", y_fc2)

    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state('./model2/')
        sess.run(tf.global_variables_initializer())
        loader = tf.train.Saver(var_list=[var for var in tf.trainable_variables() if not var.name.startswith("fc2")],
                               max_to_keep=4)
        print(ckpt)
        if ckpt != None:
            if os.path.exists(ckpt.model_checkpoint_path):
                print('restored')
                loader.restore(sess, ckpt.model_checkpoint_path)
        X, Y = data_set.read_data_set(super_params['train_set_path'], input_height, input_width, input_chaneel,
                                      super_params['out_length'])
        batch_size = super_params['batch_size']
        print()
        print('\n')
        print(batch_size)
        print(super_params['epoch'])
        index = 0
        saver = tf.train.Saver(max_to_keep=4)
        for epoch in range(int(super_params['epoch'])):
            while True:
                if index + batch_size >= epoch:
                    input_x = X[index: epoch]
                    input_y = Y[index: epoch]
                    index = 0
                    l = list(zip(X, Y))
                    np.random.shuffle(l)
                    X, Y = zip(*l)
                    train_step.run(feed_dict={x: input_x, y_: input_y})
                    break
                else:
                    input_x = X[index:index + batch_size]
                    input_y = Y[index:index + batch_size]
                    index += batch_size
                train_step.run(feed_dict={x: input_x, y_: input_y})

            train_accuracy = accuracy.eval(feed_dict={x: X, y_: Y})
            train_loss = cross_entropy_loss.eval(feed_dict={x: X, y_: Y})
            step_info = "epoch:{} loss: {:.5f} accuracy:{:.5f}".format(epoch, train_loss, train_accuracy)
            status_handler.handleTrainStep(url, id, step_info)
            log.append(step_info)
            print(step_info)
            if epoch % 10 == 0:
                print('save')
                saver.save(sess, "./model2/my-model", global_step=epoch)
            if train_accuracy > 0.98 & (train_loss < 0.001) :
                break
                # saver.save(sess, "../model2/my-model", global_step=epoch)
        saver.save(sess, "./model2/my-model", global_step=epoch)
    return log

def load_model(super_params):
    X, Y = data_set.read_data_set('E:/vscodeworkspace/FaceRecognition/train', 128, 128, 3, 10)
    with tf.Session() as sess:
        # load the meta graph and weights
        saver = tf.train.import_meta_graph('model1/my-model-90.meta')
        saver.restore(sess, tf.train.latest_checkpoint("model1/"))
        # get weights
        graph = tf.get_default_graph()
        fc2_w = graph.get_tensor_by_name("fc2/w:0")
        fc2_b = graph.get_tensor_by_name("fc2/b:0")

        print("------------------------------------------------------")
        print(sess.run(fc2_w))
        print("#######################################")
        print(sess.run(fc2_b))
        print("------------------------------------------------------")

        input_x = graph.get_operation_by_name("x").outputs[0]

        feed_dict = {"x:0":X, "y_:0":Y}
        y = graph.get_tensor_by_name("y_:0")
        yy = sess.run(y, feed_dict)
        print(yy)
        print("the answer is: ", sess.run(tf.argmax(yy, 1)))
        print("------------------------------------------------------")

        pred_y = tf.get_collection("predict")
        pred = sess.run(pred_y, feed_dict)[0]
        print(pred, '\n')

        pred = sess.run(tf.argmax(pred, 1))
        print("the predict is: ", pred)
        print("------------------------------------------------------")

        acc = graph.get_tensor_by_name("accuracy:0")
        acc = sess.run(acc, feed_dict)
        print("the accuracy is: ", acc)
        print("------------------------------------------------------")

# train_model()
# load_model()
# with tf.Session() as sess:
#     print(tf.train.get_checkpoint_state('./model1/'))
#     print(tf.train.get_checkpoint_state('./model1/').model_checkpoint_path)
