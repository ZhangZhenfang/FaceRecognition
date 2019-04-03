from PIL import Image
import numpy as np
import os

def read_train(path) :
    for f in os.listdir(path) :
        image_open = Image.open(path + "/" + f)
        array = np.array(image_open)
        length = np.size(array)
        width = np.size(array[0])
        height = int(length / width)
        break
    len1 = len(os.listdir(path))
    train = np.empty((len1, length))
    labels = np.empty((len1, 40))
    i = 0
    for f in os.listdir(path) :
        image_open = Image.open(path + "/" + f)
        array = np.array(image_open) / 256
        reshape = array.reshape([length])
        train[i] = reshape
        zeros = np.zeros(40)
        end = f.index("_")
        zeros[int(f[1:end]) - 1] = 1
        labels[i] = zeros
        i += 1
        print(f)
        print(int(f[1:end]) - 1)
    return (width, height, train, labels)
