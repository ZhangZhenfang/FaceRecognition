import os
from PIL import Image
import numpy as np
import Properties
# path = "E:/faces/s1"
# color = "E:/faces/color/source0-99/000"
#
# image_open = Image.open(path + "/10.jpg")
# colored = Image.open(color + "/000_0.bmp")
# convert = image_open.convert("RGB")
# array1 = np.array(colored)
# array2 = np.array(convert)
# array3 = np.array(image_open)
# print(image_open.mode)
# print(image_open.chanel)
# print(colored.size)
# print(array2)
# print(array3)

parse = Properties.parse("E:/vscodeworkspace/FaceRecognition/FaceRecognitionCore/super_parms.properties")
print(parse.get("train_path"))
print(parse.get("test_path"))
