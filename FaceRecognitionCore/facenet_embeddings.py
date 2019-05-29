import tensorflow as tf
import facenet
import time
from data_set import DataSetFromNameList
import numpy as np
import os
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
        e = Embedding()
        src = os.listdir(src_path)
        src_npy = []
        for i in src:
            src_npy.append(i + ".npy")
        npy = os.listdir(npy_path)
        sub = set(npy) - set(src_npy)
        for i in sub:
            os.remove(npy_path + "/" + i)
        sub = set(src_npy) - set(npy)
        list_to_encode = []
        for i in sub:
            list_to_encode.append(i[0:i.index(".npy")])
        # print(list_to_encode)
        data = DataSetFromNameList(src_path, list_to_encode, 1, (160, 160, 3), 100)
        # print(data.size)
        while data.is_end():
            x, y, names = data.next_bath()
            es = e.get_embeddings(x)
            i = 0
            for name in names:
                np.save(npy_path + "/" + name + ".npy", es[i])
                i += 1
# src_path = 'E:/vscodeworkspace/FaceRecognition/train'
# npy_path = 'E:/vscodeworkspace/FaceRecognition/trainnpy'
# embedding(src_path, npy_path)

# data = DataSet("E:\\vscodeworkspace\\FaceRecognition\\train", 1, (160, 160, 3), 3)
# x, y = data.next_bath()
#
# print(get_embeddings(x))
