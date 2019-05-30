# -*- coding: utf-8 -*-
# @Time    : 2018/6/1 20:34
# @File    : server.py
# @Software: PyCharm
import tensorflow as tf
import facenet
import base64
import numpy as np
import cv2


def get_feature():
    modeldir = './model/20170512-110547.pb'  # change to your model dir
    tf.Graph().as_default()
    sess = tf.Session()
    facenet.load_model(modeldir)
    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
    def computeFeatureBytes(imageB64):
        """
        :param imageB64: 图片base64编码
        :return: 返回128纬特征向量 list
        """
        image_size = 299  # don't need equal to real image size, but this value should not small than this

        embedding_size = embeddings.get_shape()[1]
        scaled_reshape = []
        # 解码base64图片
        nparr = np.fromstring(base64.b64decode(imageB64), np.uint8)
        img = cv2.imdecode(nparr, cv2.COLOR_BGR2RGB)

        image = cv2.resize(img, (image_size, image_size), interpolation=cv2.INTER_CUBIC)
        image = facenet.prewhiten(image)
        scaled_reshape.append(image.reshape(-1, image_size, image_size, 3))
        emb_array = np.zeros((1, embedding_size))
        emb_array[0, :] = \
        sess.run(embeddings, feed_dict={images_placeholder: scaled_reshape[0], phase_train_placeholder: False})[0]

        return emb_array[0].tolist()
    return computeFeatureBytes

