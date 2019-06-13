import tensorflow as tf
import pandas as pd
import numpy as np
import random

IMAGE_SIZE = 48
CLIPED_SIZE = 42
EMO_NUM = 7
NUM_CHANNEL = 1
SAVE_PATH = './saved_model'


def GetSymmetric(pixel, size):
    '''
    pixel: np.array with shape (count,size,size,1); 
    size: picture size; 
    return: symmetric np.array with shape (count,size,size,1); 
    '''
    count = pixel.shape[0]
    sym = np.zeros((count, size, size, NUM_CHANNEL))
    for i in range(count):
        for j in range(size):
            for k in range(size):
                sym[i, j, k, 0] = pixel[i, j, size - k - 1, 0]
    return sym


def GetClippedImage(pixel, start):
    '''
    pixel: raw 48*48 pixel data with shape (count, 48, 48, 1); 
    start: a tuple such as (0,0),(2,3),(4,2), represents start point of clipped 42*42 image; 
    returns: clipped 42*42 pixel data with shape (count, 42, 42, 1); 
    '''
    count = pixel.shape[0]
    out = np.zeros((count, CLIPED_SIZE, CLIPED_SIZE, NUM_CHANNEL))
    for i in range(count):
        for j in range(CLIPED_SIZE):
            out[i, j, :, 0] = pixel[i, start[0] + j, start[1]:start[1] + CLIPED_SIZE, 0]
    return out


def DataPreprocess(pixel):
    '''
    pixel: pixel data with shape (count,48,48,1); 
    label: optical, corresponding label of pixel; 
    '''
    a = random.randint(0, 2)
    b = random.randint(3, 5)
    c = random.randint(0, 2)
    d = random.randint(3, 5)
    pixel1 = GetClippedImage(pixel, (a, c))
    pixel2 = GetClippedImage(pixel, (a, d))
    pixel3 = GetClippedImage(pixel, (b, c))
    pixel4 = GetClippedImage(pixel, (b, d))
    out_p = np.concatenate((pixel1, pixel2, pixel3, pixel4), axis=0)
    return out_p


class CNNModel:
    def __init__(self):
        self.sess = tf.Session()
        loader = tf.train.import_meta_graph(SAVE_PATH + '.meta')
        loader.restore(self.sess, SAVE_PATH)

        self.loaded_graph = tf.get_default_graph()
        self.load_x = self.loaded_graph.get_tensor_by_name('INPUT:0')
        self.load_y = self.loaded_graph.get_tensor_by_name('LABEL:0')
        self.load_log = self.loaded_graph.get_tensor_by_name('LOGITS:0')
        self.load_keep = self.loaded_graph.get_tensor_by_name('KEEP:0')

    def __del__(self):
    	self.sess.close()

    def predict(self, pixel):
        # Pre-processing
        max = pixel.max() + 0.001
        for i in range(IMAGE_SIZE):
            pixel[i] = pixel[i] / max
        pixel = pixel.reshape((1, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNEL))
        in_data = DataPreprocess(pixel)
        in_data = np.concatenate((in_data, GetSymmetric(in_data, CLIPED_SIZE)), axis=0)

        logit = self.sess.run(self.load_log, feed_dict={
            self.load_x: in_data, self.load_y: np.zeros((8, EMO_NUM)), self.load_keep: 1.0
        })

        log = np.zeros((1, EMO_NUM))
        for i in range(8):
            log += logit[i]
        g = tf.Graph()
        with g.as_default():
            op = tf.nn.softmax(log)
        with tf.Session(graph=g) as sess:
            log = sess.run(op)

        return log
