from PIL import Image
import numpy as np
import os
def read_train(path) :
    len1 = len(os.listdir(path))
    train = np.empty((len1, 2304))
    labels = np.empty((len1, 40))
    i = 0
    for f in os.listdir(path) :
        image_open = Image.open(path + "/" + f)
        array = np.array(image_open) / 256
        reshape = array.reshape([2304])
        train[i] = reshape
        zeros = np.zeros(40)
        end = f.index("_")
        zeros[int(f[1:end]) - 1] = 1
        labels[i] = zeros
        i += 1
    return (train, labels)
