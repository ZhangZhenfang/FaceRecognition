import tensorflow as tf
import facenet
import time
from data_set import DataSet
import numpy as np
model_dir = './models/20170512-110547/20170512-110547.pb'


class Embedding:
    def __init__(self):
        tf.Graph().as_default()
        facenet.load_model(model_dir)
        self.embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        self.input_x = tf.get_default_graph().get_tensor_by_name("input:0")
        self.phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        self.sess = tf.Session()

    def get_embeddings(self, x):
        start = time.time()
        e = self.sess.run(self.embeddings, feed_dict={self.input_x: x, self.phase_train_placeholder: False})
        print(time.time() - start)
        return e

    def embedding(self, src_path, npy_path):
        data = DataSet(src_path, 1, (160, 160, 3), 100)
        print(data.size)
        while data.is_end():
            x, y, names = data.next_bath()
            es = self.get_embeddings(x)
            i = 0
            for name in names:
                np.save(npy_path + "/" + name + ".npy", es[i])
                i += 1
# data = DataSet("E:\\vscodeworkspace\\FaceRecognition\\train", 1, (160, 160, 3), 3)
# x, y = data.next_bath()
#
# print(get_embeddings(x))
