from PIL import Image
import numpy as np
import os

def read_train(path, result_length) :
    for f in os.listdir(path) :
        image_open = Image.open(path + "/" + f)
        array1 = np.array(image_open)
        length = np.size(array1)
        channel = np.size(array1[0][0])
        width = int(np.size(array1[0]) / channel)
        height = int(length / width / channel)
        break
    len1 = len(os.listdir(path))
    train = np.empty((len1, height, width, 3))
    labels = np.empty((len1, result_length))
    i = 0
    for f in os.listdir(path) :
        print(f)
        image_open = Image.open(path + "/" + f)
        if image_open.mode == "L" :
            image_open = image_open.convert("RGB")
        array = np.array(image_open) / 256
        train[i] = array
        zeros = np.zeros(result_length)
        end = f.index("_")
        zeros[int(f[1:end]) - 1] = 1
        labels[i] = zeros
        i += 1
    return (width, height, channel, train, labels)
# read_train("E:/faces/train", 40)
