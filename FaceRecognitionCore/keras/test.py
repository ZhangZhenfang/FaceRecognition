import new_model
import tensorflow as tf
import data_set

# 连同图结构一同加载
ckpt = tf.train.get_checkpoint_state('../model1/')
saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path +'.meta')
X, Y = data_set.read_data_set('E:/vscodeworkspace/FaceRecognition/train', 128, 128, 3, 10)
with tf.Session() as sess:
    saver.restore(sess,ckpt.model_checkpoint_path)
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
