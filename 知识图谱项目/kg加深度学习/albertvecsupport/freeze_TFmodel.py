#!/usr/bin/python
# -*- coding:utf-8 -*-
# 生成TensorFlow pb模型文件供Java工程使用

from bert4keras.models import build_transformer_model
import tensorflow as tf
from keras import backend as K
from tensorflow.python.framework import graph_util, graph_io
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def export_graph(model, export_path, output_name):
    '''

    :param model: keras模型对象
    :param export_path: 导出路径
    :param output_name: 导出pb文件的名称——output_name.pb
    :return: 模型的输入、输出Tensor名称——input_names, input_nodes

    '''
    input_names = model.input_names

    if not tf.gfile.Exists(export_path):
        tf.gfile.MakeDirs(export_path)

    with K.get_session() as sess:
        init_graph = sess.graph
        with init_graph.as_default():
            output_names = []

            for i in range(len(model.outputs)):
                output_names.append("output_" + str(i + 1))
                tf.identity(model.output[i], "output_" + str(i + 1))

            init_graph = sess.graph.as_graph_def()
            main_graph = graph_util.convert_variables_to_constants(sess, init_graph, output_names)
            graph_io.write_graph(main_graph, export_path, name='%s.pb' % output_name, as_text=False)

    return input_names, output_names


if __name__ == '__main__':
    config_path = 'model/albert_tiny_zh_google/albert_config_tiny_g.json'
    checkpoint_path = 'model/albert_tiny_zh_google/albert_model.ckpt'
    dict_path = 'model/albert_tiny_zh_google/vocab.txt'
    output_path = "output/"
    model = build_transformer_model(config_path, checkpoint_path, model='albert', with_pool=True)  # 建立模型，加载权重
    inputs, outputs = export_graph(model, output_path, "albert_tiny_zh_google")
    print("input_names:" + str(inputs))
    print("output_names:" + str(outputs))
