import tensorflow as tf
import facenet


class ModelBasedFaceNetAndFcNet:
    def __init__(self, facenet_model_path, fcnet_model_path):
        self.fcnet_model_path = fcnet_model_path
        self.facenet_model_path = facenet_model_path
        self.embeddings = None
        self.input_x = None
        self.phase_train_placeholder = None
        self.x = None
        self.out = None
        self.keep_prob = None
        self.sess = None
        self.tf = tf
        self.load()

    def load(self):
        tf.reset_default_graph()
        tf.Graph().as_default()
        if self.sess:
            self.sess.close()
        self.sess = tf.Session()
        facenet.load_model(self.facenet_model_path)
        self.embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        self.input_x = tf.get_default_graph().get_tensor_by_name("input:0")
        self.phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

        ckpt = tf.train.get_checkpoint_state(self.fcnet_model_path)
        saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path + '.meta')
        saver.restore(self.sess, ckpt.model_checkpoint_path)
        self.x = tf.get_default_graph().get_tensor_by_name("x:0")
        self.out = tf.get_default_graph().get_tensor_by_name("fc3/out:0")
        self.keep_prob = tf.get_default_graph().get_operation_by_name("keep_prob").outputs[0]

    def predict(self, x, keep_prob):
        e = self.sess.run(self.embeddings, feed_dict={self.input_x: x, self.phase_train_placeholder: False})
        res = self.sess.run(self.out, feed_dict={self.x: e, self.keep_prob: keep_prob})
        return res

# model = ModelBasedFaceNetAndFcNet('./models/20170512-110547/20170512-110547.pb', "./models/facenet_based_face_model_fc/")
# data = DataSet("E:\\vscodeworkspace\\FaceRecognition\\train",
#                         1,
#                         (160, 160, 3),
#                         3)
# x, y, z = data.next_bath()
# predict = model.predict(x, 1.0)
# print(predict)
