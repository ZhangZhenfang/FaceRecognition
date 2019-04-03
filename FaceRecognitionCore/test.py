import os
from PIL import Image

path = "E:/faces"

for d in os.listdir(path) :
    if d.endswith("10.jpg") :
        image_open = Image.open(path + "/" + d)
        image_open.save(path + "/test/" + d)
