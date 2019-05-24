import cv2
import os
import numpy as np
from PIL import Image

import sys

import dlib


predictor_path = "D:\\shape_predictor_68_face_landmarks.dat"
face_file_path = '‪C:/Users/fang/Desktop/201904300943090.jpg'

# Load all the models we need: a detector to find the faces, a shape predictor
# to find face landmarks so we can precisely localize the face
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)

# Load the image using Dlib
# img = dlib.load_rgb_image(face_file_path)

# img = Image.open('201904300943090.jpg')
img = cv2.imread('201904300943091.jpg')
# Ask the detector to find the bounding boxes of each face. The 1 in the
# second argument indicates that we should upsample the image 1 time. This
# will make everything bigger and allow us to detect more faces.
dets = detector(img, 1)

num_faces = len(dets)
if num_faces == 0:
    print("Sorry, there were no faces found in '{}'".format(face_file_path))
    exit()

# Find the 5 face landmarks we need to do the alignment.
faces = dlib.full_object_detections()
for detection in dets:
    faces.append(sp(img, detection))

window = dlib.image_window()

# Get the aligned face images
# Optionally:
# images = dlib.get_face_chips(img, faces, size=160, padding=0.25)
images = dlib.get_face_chips(img, faces, size=320)
i = 0
for image in images:
    cv2.imwrite(str(i) + ".jpg", image)
    i += 1

# It is also possible to get a single chip
image = dlib.get_face_chip(img, faces[0])
window.set_image(image)
dlib.hit_enter_to_continue()



















