import data_set
import tensorflow as tf
import numpy as np
# train_path = "E:/faces/train"
# test_path = "E:/faces/test"

# train_path = "E:/faces/color/64/colortrain"
# test_path = "E:/faces/color/64/colortest"

label_length = 40
width, height, channel, train, labels = data_set.read_train(train_path, label_length)
print(width, height)
_, _, _, test, test_labels = data_set.read_train(test_path, label_length)

# 定义输入数据
x = tf.placeholder(tf.float32, shape=[None, height, width, 3])
# 定义输出数据
y_ = tf.placeholder(tf.float32, shape=[None, label_length])

# x_image = tf.reshape(x, [-1, height, width, 3])
keep_prob = tf.placeholder(tf.float32)
# 卷积层1卷积核
W_conv1 = tf.Variable(tf.truncated_normal([3, 3, 3, 32], stddev=0.1))
# 卷积层1偏置
b_conv1 = tf.constant(0.1, shape=[32])

# 卷积层1卷积后经过激活函数relu的结果
h_conv1 = tf.nn.relu(tf.nn.conv2d(x, W_conv1, strides=[1, 1, 1, 1], padding='SAME') + b_conv1)
# 进行卷积层1的池化操作
h_pool1 = tf.nn.max_pool(h_conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
# h_pool1 = tf.nn.dropout(h_pool1, keep_prob)
# 卷积层2卷积核
W_conv2 = tf.Variable(tf.truncated_normal([3, 3, 32, 64], stddev=0.1))
# 卷积层2偏置
b_conv2 = tf.constant(0.1, shape=[64])

# 卷积层2卷积后经过relu激活函数的结果
h_conv2 = tf.nn.relu(tf.nn.conv2d(h_pool1, W_conv2, strides=[1, 1, 1, 1], padding='SAME') + b_conv2)
# 进行卷积层2池化操作
h_pool2 = tf.nn.max_pool(h_conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
# h_pool2 = tf.nn.dropout(h_pool2, keep_prob)

W_conv3 = tf.Variable(tf.truncated_normal([3, 3, 64, 64], stddev=0.1))
b_conv3 = tf.constant(0.1, shape=[64])

h_conv3 = tf.nn.relu(tf.nn.conv2d(h_pool2, W_conv3, strides=[1, 1, 1, 1], padding='SAME') + b_conv3)
h_pool3 = tf.nn.max_pool(h_conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
h_pool3 = tf.nn.dropout(h_pool3, keep_prob)
# 全连接层1权重定义
W_fc1 = tf.Variable(tf.truncated_normal([14 * 12 * 64, 512], stddev=0.1))
# 全连接层1偏置定义
b_fc1 = tf.constant(0.1, shape=[512])

# 对卷积层2的输出展开
h_pool3 = tf.reshape(h_pool3, [-1, 14 * 12 * 64])
# 全连接层1，上一层的输出矩阵乘权重后加偏置后经过激活函数
h_fc1 = tf.nn.relu(tf.matmul(h_pool3, W_fc1) + b_fc1)

# dropout可解决过拟合问题

h_fc1 = tf.nn.dropout(h_fc1, keep_prob)

# 全连接层2权重
W_fc2 = tf.Variable(tf.truncated_normal([512, label_length], stddev=0.1))
# 全连接层2偏置
b_fc2 = tf.constant(0.1, shape=[label_length])

# 输出
y_conv = tf.matmul(h_fc1, W_fc2) + b_fc2

# 交叉熵
cross_entry = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
# 选择优化器对交叉熵进行最小化优化
train_step = tf.train.AdamOptimizer(1e-3).minimize(cross_entry)

# 计算正确的个数，向量对应的位置的数进行比较，相等则对应位置为True
y_max = tf.argmax(y_, 1)
y_conv_max = tf.argmax(y_conv, 1)
# 预测值
prediction = tf.argmax(y_conv, 1)
correct_prediction = tf.equal(y_max, y_conv_max)
# 计算训练准确率，将True转为1，然后计算平均值
train_accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

saver = tf.train.Saver()

with tf.Session() as sess :
    sess.run(tf.global_variables_initializer())
    for i in range(2000) :
        if i % 4 == 0 :
            l = list(zip(train, labels))
            np.random.shuffle(l)
            train, labels = zip(*l)
        start = (i * 90) % 360
        end = (start + 90)
        input_x = train[start:end]
        input_y = labels[start:end]
        _, accuracy = sess.run([train_step, train_accuracy],
            feed_dict={x: input_x, y_: input_y, keep_prob: 0.5})
        # saver.save(sess, './mnist_model/model.ckpt')
        l = list(zip(test, test_labels))
        np.random.shuffle(l)
        test, test_labels = zip(*l)
        b_fc2_, y_max_, y_conv_max_, train_accuracy_ = sess.run([b_fc2, y_max, y_conv_max, train_accuracy, ],
                                                                feed_dict={x: test, y_: test_labels, keep_prob: 1.0})
        print("%g" %i, accuracy, train_accuracy_)
