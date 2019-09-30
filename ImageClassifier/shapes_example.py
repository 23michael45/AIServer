# coding: utf-8


import tensorflow as tf
import os
import random
import math
import sys
import types
from PIL import Image
import sys
import os
print(os.name)
if os.name == "nt":
    print('nt')
    TensorflowPath = 'D:/DevelopProj/Tensorflow/'
    DatasetsPath = 'D:/DevelopProj/Dadao/ESP32Project/Datasets/'
else:
    TensorflowPath = '/media/jerry/f0bb2ff2-cab9-46b3-8e2b-beae1c413d67/DevelopProj/Thirdparty/Tensorflow/'
    DatasetsPath = '/media/jerry/f0bb2ff2-cab9-46b3-8e2b-beae1c413d67/DevelopProj/Dadao/ESP32Project/Datasets/'

sys.path.append(TensorflowPath + 'models/research/')
sys.path.append(TensorflowPath + 'models/research/slim')
import slim

def tfrecord():
    import download_and_convert_shapes
    sys.argv.append('--dataset_name=shapes')
    sys.argv.append('--dataset_dir=' + DatasetsPath +'Shapes/Dst')
    download_and_convert_shapes.main()


def train():
    import slim
    import datasets.dataset_factory
    import shapes
    
    datasets.dataset_factory.datasets_map['shapes'] = shapes

    import slim.train_image_classifier
    sys.argv.append('--train_dir=' + DatasetsPath + 'Shapes/Dst/train')
    sys.argv.append('--dataset_name=shapes')
    sys.argv.append('--dataset_split_name=train')
    sys.argv.append('--dataset_dir=' + DatasetsPath + 'Shapes/Dst/tfrecord')
    sys.argv.append('--batch_size=5')
    sys.argv.append('--max_number_of_steps=10000')
    sys.argv.append('--model_name=inception_v3')
    sys.argv.append('--clone_on_cpu=true')
    sys.argv.append('--checkpoint_path=' + TensorflowPath + 'pretrained/inception_v3.ckpt')
    sys.argv.append('--checkpoint_exclude_scopes=InceptionV3/Logits,InceptionV3/AuxLogits')
    sys.argv.append('--trainable_scopes=InceptionV3/Logits,InceptionV3/AuxLogits')

    slim.train_image_classifier.main(sys.argv)
def eval():
    import slim
    import datasets.dataset_factory
    import shapes
    
    datasets.dataset_factory.datasets_map['shapes'] = shapes

    import slim.eval_image_classifier
    sys.argv.append('--dataset_name=shapes')
    sys.argv.append('--checkpoint_path=' + DatasetsPath + 'Shapes/Dst/train')     # fine-tuning位置
    sys.argv.append('--dataset_dir=' + DatasetsPath + 'Shapes/Dst/tfrecord')
    sys.argv.append('--dataset_split_name=test')
    sys.argv.append('--model_name=inception_v3')
    sys.argv.append('--batch_size=5')

    slim.eval_image_classifier.main(sys.argv)


if __name__ == '__main__':
    #tfrecord()
    train()
    #eval()
