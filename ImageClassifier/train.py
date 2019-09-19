# coding: utf-8


import tensorflow as tf
import os
import random
import math
import sys
import types
from PIL import Image
import sys

sys.path.append('D:/DevelopProj/Tensorflow/models/research/')
sys.path.append('D:/DevelopProj/Tensorflow/models/research/slim')
import slim
import datasets.dataset_factory
import slim.train_image_classifier

import cards

datasets.dataset_factory.datasets_map['cards'] = cards


sys.argv.append('--train_dir=D:/DevelopProj/Dadao/ESP32Project/Datasets/Image80/Dst/train')
sys.argv.append('--dataset_name=cards')
sys.argv.append('--dataset_split_name=train')
sys.argv.append('--dataset_dir=D:/DevelopProj/Dadao/ESP32Project/Datasets/Image80/Dst/tfrecord')
sys.argv.append('--batch_size=5')
sys.argv.append('--max_number_of_steps=10000')
sys.argv.append('--model_name=inception_v3')
sys.argv.append('--clone_on_cpu=true')

slim.train_image_classifier.main(sys.argv)
