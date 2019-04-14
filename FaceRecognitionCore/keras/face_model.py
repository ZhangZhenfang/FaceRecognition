import tensorflow as tf
import numpy as np
import os

def load_data(resultpath):

    datapath = os.path.join(resultpath, "data10_4.npz")
    if os.path.exists(datapath):
        data = np.load(datapath)
        X, Y = data["X"], data["Y"]
    else:
        X = np.array(np.arange(30720)).reshape(10, 32, 32, 3)
        Y = [0, 0, 1, 1, 2, 2, 3, 3, 2, 0]
        X = X.astype('float32')
        Y = np.array(Y)
        np.savez(datapath, X=X, Y=Y)
        print('Saved dataset to dataset.npz.')
    print('X_shape:{}\nY_shape:{}'.format(X.shape, Y.shape))
    return X, Y

def define_model(x):

    x_image = tf.reshape(x, [-1, 32, 32, 3])
    print(x_image.shape)

    def weight_variable(shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial, name="w")

    def bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial, name="b")

    def conv3d(x, W):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2d(x):
        return tf.nn.max_pool(x, ksize=[1, 3, 3, 1], strides=[1, 3, 3, 1], padding='SAME')

    with tf.variable_scope("conv1"):  # [-1,32,32,3]
        weights = weight_variable([3, 3, 3, 32])
        biases = bias_variable([32])
        conv1 = tf.nn.relu(conv3d(x_image, weights) + biases)
        pool1 = max_pool_2d(conv1)  # [-1,11,11,32]

    with tf.variable_scope("conv2"):
        weights = weight_variable([3, 3, 32, 64])
        biases = bias_variable([64])
        conv2 = tf.nn.relu(conv3d(pool1, weights) + biases)
        pool2 = max_pool_2d(conv2) # [-1,4,4,64]

    with tf.variable_scope("fc1"):
        weights = weight_variable([4 * 4 * 64, 128]) # [-1,1024]
        biases = bias_variable([128])
        fc1_flat = tf.reshape(pool2, [-1, 4 * 4 * 64])
        fc1 = tf.nn.relu(tf.matmul(fc1_flat, weights) + biases)
        fc1_drop = tf.nn.dropout(fc1, 0.5) # [-1,128]

    with tf.variable_scope("fc2"):
        weights = weight_variable([128, 4])
        biases = bias_variable([4])
        fc2 = tf.matmul(fc1_drop, weights) + biases # [-1,4]

    return fc2

def train_model():

    x = tf.placeholder(tf.float32, shape=[None, 32, 32, 3], name="x")
    y_ = tf.placeholder('int64', shape=[None], name="y_")

    initial_learning_rate = 0.001
    y_fc2 = define_model(x)
    y_label = tf.one_hot(y_, 4, name="y_labels")

    loss_temp = tf.losses.softmax_cross_entropy(onehot_labels=y_label, logits=y_fc2)
    cross_entropy_loss = tf.reduce_mean(loss_temp)

    train_step = tf.train.AdamOptimizer(learning_rate=initial_learning_rate, beta1=0.9, beta2=0.999,
                                        epsilon=1e-08).minimize(cross_entropy_loss)

    correct_prediction = tf.equal(tf.argmax(y_fc2, 1), tf.argmax(y_label, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # save model
    saver = tf.train.Saver(max_to_keep=4)
    tf.add_to_collection("predict", y_fc2)

    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())
        print("------------------------------------------------------")
        X, Y = load_data("model1/")
        X = np.multiply(X, 1.0 / 255.0)
        for epoch in range(200):

            if epoch % 10 == 0:
                print("------------------------------------------------------")

                train_accuracy = accuracy.eval(feed_dict={x: X, y_: Y})
                train_loss = cross_entropy_loss.eval(feed_dict={x: X, y_: Y})

                print("after epoch %d, the loss is %6f" % (epoch, train_loss))
                print("after epoch %d, the acc is %6f" % (epoch, train_accuracy))

                saver.save(sess, "model1/my-model", global_step=epoch)
                print("save the model")

            train_step.run(feed_dict={x: X, y_: Y})

        print("------------------------------------------------------")

def load_model():

    # prepare the test data
    X = np.array(np.arange(6144, 12288)).reshape(2, 32, 32, 3)
    Y = [3, 1]
    Y = np.array(Y)
    X = X.astype('float32')
    X = np.multiply(X, 1.0 / 255.0)
    with tf.Session() as sess:

        # load the meta graph and weights
        saver = tf.train.import_meta_graph('model1/my-model-190.meta')
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
        y = graph.get_tensor_by_name("y_labels:0")
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

        acc = graph.get_operation_by_name("acc")
        acc = sess.run(acc, feed_dict)
        print("the accuracy is: ", acc)
        print("------------------------------------------------------")

#train_model()
load_model()
