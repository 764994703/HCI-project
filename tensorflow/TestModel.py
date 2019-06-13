import pandas as pd
import numpy as np
from FER import test


'''
Accuracy : 0.679
'''


IMAGE_SIZE = 48
CLIPED_SIZE = 42
EMO_NUM = 7
TRAIN_SIZE = 4 * (35887 * 2 - 10000)
VALID_SIZE = 1500
TEST_SIZE = 5000
BATCH_SIZE = 50
NUM_CHANNEL = 1
EPOCHS = 50
SAVE_PATH = './saved_model'
emo_dict = {
    0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Suprise', 6: 'Neutral'
}


def get_test_data():
    all_data = pd.read_csv('fer2013.csv')
    label = np.array(all_data['emotion'])
    data = np.array(all_data['pixels'])
    sample_count = len(label)  # should be 35887

    pixel_data = np.zeros((sample_count, IMAGE_SIZE * IMAGE_SIZE))  # 像素点数据
    label_data = np.zeros((sample_count, EMO_NUM), dtype=int)  # 标签数据，独热
    for i in range(sample_count):
        x = np.fromstring(data[i], sep=' ')
        max = x.max()
        x = x / (max + 0.001)  # 灰度归一化
        pixel_data[i] = x
        label_data[i, label[i]] = 1
    pixel_data = pixel_data.reshape(sample_count, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNEL)
    x_test = pixel_data[30000:35000]
    y_test = label_data[30000:35000]
    return (x_test, y_test)


def main():
    (x_test, y_test) = get_test_data()
    print("Start testing")
    test(x_test, y_test)


if __name__ == '__main__':
    main()
