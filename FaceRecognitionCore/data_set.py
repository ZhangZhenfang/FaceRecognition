from PIL import Image
import numpy as np
import os


def read_data_set(path, height, width, channel, result_length) :
    len1 = len(os.listdir(path))
    train = np.empty((len1, height, width, channel))
    labels = np.empty((len1, result_length))
    i = 0
    for f in os.listdir(path) :
        image_open = Image.open(path + "/" + f)
        if image_open.mode == "L" :
            image_open = image_open.convert("RGB")
        array = np.array(image_open) / 255
        train[i] = array
        zeros = np.zeros(result_length)
        end = f.index("_")
        # 转为One-Hot编码格式
        zeros[int(f[0:end]) - 1] = 1
        labels[i] = zeros
        i += 1
    return (train, labels)

def read_data_set3(path, height, width, channel, result_length) :
    len1 = len(os.listdir(path))
    train = np.empty((len1, height, width, channel))
    labels = np.empty((len1, result_length))
    i = 0
    for f in os.listdir(path) :
        # print(f)
        # print(result_length)
        image_open = Image.open(path + "/" + f)
        if image_open.mode == "L" :
            image_open = image_open.convert("RGB")
        array = np.array(image_open) / 255
        train[i] = array
        zeros = np.zeros(result_length)
        end = f.index("_")
        # print(end)
        # zeros[int(f[0:end]) - 1] = 1
        zeros[int(f[0:end])] = 1
        labels[i] = zeros
        i += 1
    return (train, labels)

def read_data_set2(path, height, width, channel, result_length) :
    len1 = len(os.listdir(path))
    train = np.empty((len1, height, width, channel))
    labels = np.empty((len1, result_length))
    i = 0
    for f in os.listdir(path) :
        print(f)
        print(result_length)
        image_open = Image.open(path + "/" + f)
        if image_open.mode == "L" :
            image_open = image_open.convert("RGB")
        array = np.array(image_open) / 255
        train[i] = array
        zeros = np.zeros(result_length)
        end = f.index("_")
        print(end)
        zeros[int(f[1:end]) - 1] = 1
        labels[i] = zeros
        i += 1
    return train, labels


def read_data(paths, height, width, channel, result_length):
    result = np.empty((len(paths), height, width, channel))
    labels = np.empty((len(paths), result_length))
    i = 0
    for f in paths:
        image_open = Image.open(f)
        if image_open.mode == "L" :
            image_open = image_open.convert("RGB")
        array = np.array(image_open) / 255
        result[i] = array
        i += 1
    return result, labels


def shuffle(train, label):
    l = list(zip(train, label))
    np.random.shuffle(l)
    train_, label_ = zip(*l)
    return train_, label_
