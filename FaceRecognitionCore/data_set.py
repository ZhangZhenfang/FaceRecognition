from PIL import Image
import numpy as np
import os
import cv2


class DataSet:
    def __init__(self, src, start_index, image_shape, batch_size):
        self.start_index = start_index
        self.src = src
        self.batch_size = batch_size
        self.set_names = os.listdir(src)
        self.size = len(self.set_names)
        self.image_shape = image_shape
        self.index = 0
        np.random.shuffle(self.set_names)

    def next_bath(self):
        if self.batch_size == 0:
            return None
        if self.index < len(self.set_names):
            if self.index + self.batch_size <= len(self.set_names):
                batch_x = np.empty((self.batch_size,) + self.image_shape)
                batch_y = np.empty(self.batch_size)
            else:
                batch_x = np.empty((len(self.set_names) - self.index,) + self.image_shape)
                batch_y = np.empty(len(self.set_names) - self.index)
            names = self.set_names[self.index:self.index + self.batch_size]
            self.read(names, batch_x, batch_y)
            self.index += self.batch_size
            return batch_x, batch_y, names
        else:
            return None

    def read(self, names, batch_x, batch_y):
        # print(names)
        # i = 0
        # for name in names:
        #     image_open = Image.open(self.src + "/" + name)
        #     if image_open.mode == "L" :
        #         image_open = image_open.convert("RGB")
        #     array = np.array(image_open) / 255
        #     batch_x[i] = array
        #     end = name.index("_")
        #     batch_y[i] = int(int(name[0:end]) - self.start_index)
        #     i += 1
        i = 0
        for name in names:
            imread = cv2.imread(self.src + "/" + name)
            # imread = cv2.cvtColor(imread, cv2.COLOR_BGR2GRAY)
            imread = imread / 255.
            imread = cv2.resize(imread, self.image_shape[0:2])
            batch_x[i] = imread
            # image_open = Image.open(self.src + "/" + name)
            # if image_open.mode == "L" :
            #     image_open = image_open.convert("RGB")
            #     image_open = image_open.resize(self.image_shape)
            # array = np.array(image_open) / 255
            # batch_x[i] = array
            end = name.index("_")
            batch_y[i] = int(int(name[0:end]) - self.start_index)
            i += 1

    def is_end(self):
        return self.index < len(self.set_names)

    def reset(self):
        self.index = 0
        np.random.shuffle(self.set_names)


class DataSetFromNpy:
    def __init__(self, src, start_index, image_shape, batch_size):
        self.start_index = start_index
        self.src = src
        self.batch_size = batch_size
        self.set_names = os.listdir(src)
        self.size = len(self.set_names)
        self.image_shape = image_shape
        self.index = 0
        np.random.shuffle(self.set_names)

    def next_bath(self):
        if self.batch_size == 0:
            return None
        if self.index < len(self.set_names):
            if self.index + self.batch_size <= len(self.set_names):
                batch_x = np.empty((self.batch_size,) + self.image_shape)
                batch_y = np.empty(self.batch_size)
            else:
                batch_x = np.empty((len(self.set_names) - self.index,) + self.image_shape)
                batch_y = np.empty(len(self.set_names) - self.index)
            names = self.set_names[self.index:self.index + self.batch_size]
            self.read(names, batch_x, batch_y)
            self.index += self.batch_size
            return batch_x, batch_y, names
        else:
            return None

    def read(self, names, batch_x, batch_y):
        i = 0
        for name in names:
            batch_x[i] = np.load(self.src + "/" + name)
            end = name.index("_")
            batch_y[i] = int(int(name[0:end]) - self.start_index)
            i += 1

    def is_end(self):
        return self.index < len(self.set_names)

    def reset(self):
        self.index = 0
        np.random.shuffle(self.set_names)


def read_data_set(path, height, width, channel, result_length, start_index):
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
        zeros[int(f[0:end]) - start_index] = 1
        labels[i] = zeros
        i += 1
    return (train, labels)


def read_data_set_without_label(path, height, width, channel, result_length) :
    len1 = len(os.listdir(path))
    train = np.empty((len1, height, width, channel))
    # labels = np.empty((len1, result_length))
    i = 0
    for f in os.listdir(path) :
        image_open = Image.open(path + "/" + f)
        if image_open.mode == "L" :
            image_open = image_open.convert("RGB")
        array = np.array(image_open) / 255
        train[i] = array
        i += 1
    return train


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

# dataset = DataSet("E:\\vscodeworkspace\\FaceRecognition\\train", 1, (128, 128, 3), 0)
# print(dataset.set_names)
# print(dataset.test_set_names)
# while dataset.is_end():
#     batch_x, batch_y = dataset.next_bath()
#     print(batch_y)
# dataset.next_bath()
# dataset.next_bath()
# dataset.next_bath()
