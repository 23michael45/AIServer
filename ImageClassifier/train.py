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

#datasets.dataset_factory.datasets_map['cards'] = cards


sys.argv.append('--train_dir=D:/DevelopProj/Dadao/ESP32Project/Datasets/Flowers/train')
sys.argv.append('--dataset_name=flowers')
sys.argv.append('--dataset_split_name=train')
sys.argv.append('--dataset_dir=D:/DevelopProj/Dadao/ESP32Project/Datasets/Flowers/tfrecord')
sys.argv.append('--batch_size=5')
sys.argv.append('--max_number_of_steps=10000')
sys.argv.append('--model_name=inception_v3')
sys.argv.append('--clone_on_cpu=true')
sys.argv.append('--checkpoint_path=D:/DevelopProj/Tensorflow/pretrained/inception_v3.ckpt')
sys.argv.append('--checkpoint_exclude_scopes=InceptionV3/Logits,InceptionV3/AuxLogits')
sys.argv.append('--trainable_scopes=InceptionV3/Logits,InceptionV3/AuxLogits')

slim.train_image_classifier.main(sys.argv)
