import cv2
import os


def hist(src_dir, dst_dir):
    for file in os.listdir(src_dir):
        img = cv2.imread(src_dir + "/" + file, 1)
        (b, g, r) = cv2.split(img)
        bH = cv2.equalizeHist(b)
        gH = cv2.equalizeHist(g)
        rH = cv2.equalizeHist(r)
        # 合并每一个通道
        result = cv2.merge((bH, gH, rH))
        cv2.imwrite(dst_dir + "/" + file, result)


def format_name(src_dir, prefix):
    for file in os.listdir(src_dir):
        if "_" not in file:
            os.rename(src_dir + "/" + file, src_dir + "/" + prefix + "_" + file)


def resize2(src_dir, height, width):
    for file in os.listdir(src_dir):
        img = cv2.imread(src_dir + "/" + file)
        if img.shape[0] != 128:
            img = cv2.resize(img, (height, width))
            cv2.imwrite(src_dir + "/" + file, img)

# img = cv2.imread("6_81.bmp")
# if img.shape[0] != 160:
#     img = cv2.resize(img, (160, 160))
#     cv2.imwrite("6_81_160.bmp", img)
# format_name("E:\\vscodeworkspace\\facedata\\data\\srcface\\0_shitiandong", "0")
# hist("C:\\Users\\fang\\Desktop\\facedata\\dataset3\\test", "C:\\Users\\fang\\Desktop\\facedata\\dataset3\\testhisted")
# hist("E:\\vscodeworkspace\\facedata\\data\\testdata", "E:\\vscodeworkspace\\facedata\\data\\testdatahisted")
# resize2("C:\\Users\\fang\\Desktop\\facedata\\dataset1\\test", 128, 128)
