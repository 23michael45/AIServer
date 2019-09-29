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
    
    import slim.download_and_convert_data
    sys.argv.append('--dataset_name=flowers')
    sys.argv.append('--dataset_dir=' + DatasetsPath +'Flowers/tfrecord')
    slim.download_and_convert_data.main(sys.argv)


def train():
    
    import slim.train_image_classifier
    sys.argv.append('--train_dir=' + DatasetsPath + 'Flowers/train')
    sys.argv.append('--dataset_name=flowers')
    sys.argv.append('--dataset_split_name=train')
    sys.argv.append('--dataset_dir=' + DatasetsPath + 'Flowers/tfrecord')
    sys.argv.append('--batch_size=5')
    sys.argv.append('--max_number_of_steps=10000')
    sys.argv.append('--model_name=inception_v3')
    sys.argv.append('--clone_on_cpu=true')
    sys.argv.append('--checkpoint_path=' + TensorflowPath + 'pretrained/inception_v3.ckpt')
    sys.argv.append('--checkpoint_exclude_scopes=InceptionV3/Logits,InceptionV3/AuxLogits')
    sys.argv.append('--trainable_scopes=InceptionV3/Logits,InceptionV3/AuxLogits')

    slim.train_image_classifier.main(sys.argv)
def eval():
    
    import slim.eval_image_classifier
    sys.argv.append('--dataset_name=flowers')
    sys.argv.append('--checkpoint_path=' + DatasetsPath + 'Flowers/train')     # fine-tuning位置
    sys.argv.append('--dataset_dir=' + DatasetsPath + 'Flowers/tfrecord')
    sys.argv.append('--dataset_split_name=validation')
    sys.argv.append('--model_name=inception_v3')
    sys.argv.append('--batch_size=5')

    slim.eval_image_classifier.main(sys.argv)
if __name__ == '__main__':
    #tfrecord()
    train()
    eval()