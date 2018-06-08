import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys


tf.app.flags.DEFINE_string("output_graph",
                           "./workspace/flowers_graph.pb",
                           "a")
tf.app.flags.DEFINE_string("output_labels",
                           "./workspace/flowers_labels.txt",
                           "b")
tf.app.flags.DEFINE_boolean("show_image",
                            True,
                            "c")

FLAGS = tf.app.flags.FLAGS


def predict(imageName):
    labels = [line.rstrip() for line in tf.gfile.GFile(FLAGS.output_labels)]

    with tf.gfile.FastGFile(FLAGS.output_graph, 'rb') as fp:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(fp.read())
        tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        logits = sess.graph.get_tensor_by_name('final_result:0')
        image = tf.gfile.FastGFile(imageName, 'rb').read()
        prediction = sess.run(logits, {'DecodeJpeg/contents:0': image})

    # print('=== predict result ===')
    # top_result = int(np.argmax(prediction[0]))
    # name = labels[top_result]
    # score = prediction[0][top_result]
    # print('%s (%.2f%%)' % (name, score * 100))

    print('=== predict result ===')
    for i in range(len(labels)):
        name = labels[i]
        score = prediction[0][i]
        print('%s (%.2f%%)' % (name, score * 100))

    max = 0
    for i in range(len(labels)):
        if prediction[0][i] > prediction[0][max]:
            max = i
            
    return labels[max]
    

