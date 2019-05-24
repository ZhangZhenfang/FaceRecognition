def saver1 (tf, sess, tag, saved_model_dir) :
    builder = tf.saved_model.builder.SavedModelBuilder(saved_model_dir)
    builder.add_meta_graph_and_variables(sess, tag)
    builder.save()

def loader1 (tf, sess, tag, saved_model_dir) :
    return tf.saved_model.loader.load(sess, tag, saved_model_dir)

def saver2 (tf, sess, tag, saved_model_dir, inputs, outputs) :
    builder = tf.saved_model.builder.SavedModelBuilder(saved_model_dir)
    signature_def = tf.saved_model.signature_def_utils.build_signature_def(inputs, outputs, 'test_signature')
    builder.add_meta_graph_and_variables(sess=sess, tags=tag, signature_def_map={'test_signature': signature_def})
    builder.save()
