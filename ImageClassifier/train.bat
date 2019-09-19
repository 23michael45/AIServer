
python train_image_classifier.py ^
--train_dir=D:/DevelopProj/Dadao/ESP32Project/Datasets/Image80/Dst/train ^
--dataset_name=card ^
--dataset_split_name=train ^
--dataset_dir=D:/DevelopProj/Dadao/ESP32Project/Datasets/Image80/Dst/tfrecord ^
--batch_size=5 ^
--max_number_of_steps=10000 ^
--model_name=inception_v3 ^
--clone_on_cpu=true ^
pause