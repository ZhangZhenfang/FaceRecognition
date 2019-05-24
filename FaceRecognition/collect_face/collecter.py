import cv2
import dlib


def detect_and_sub_video(video_path, dst_dir, prefix):
    cap = cv2.VideoCapture(video_path)
    # face_classifier = cv2.CascadeClassifier(r'D:/openCV/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
    dlib_face_detector = dlib.get_frontal_face_detector()
    # dlib_face_detector = dlib.cnn_face_detection_model_v1()
    sp = dlib.shape_predictor("D:\\shape_predictor_68_face_landmarks.dat")
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        # if frame:
        #     break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        x, y = frame.shape[0:2]

        # 缩放到原来的二分之一，输出尺寸格式为（宽，高）
        frame = cv2.resize(frame, (int(y / 2), int(x / 2)))
        cv2.imshow('frame',frame)
        if i % 50 == 0:
            # faces = face_classifier.detectMultiScale(frame, scaleFactor=1.15, minNeighbors=5, minSize=(100, 100))
            # for(x, y, w, h) in faces:
            #     rect = frame[y: y + h, x:x + w]
            #     rect = cv2.resize(rect, (128, 128))
            #     cv2.imwrite("E:/vscodeworkspace/facedata/data/dth04/opencv/" + str(i) + ".bmp", rect)
            #     # cv2.rectangle(frame, (x,y),(x+w,y+w),(0,255,0),2)
            #     # cv2.imshow('frame',frame)

            dets = dlib_face_detector(frame, 1)
            faces = dlib.full_object_detections()
            if len(dets) != 0:
                for detection in dets:
                    faces.append(sp(frame, detection))
                    # rect = frame[det.top():det.bottom(), det.left():det.right()]
                    # rect = cv2.resize(rect, (128, 128))
                    # cv2.imwrite("E:/vscodeworkspace/facedata/data/dth06/dlib/" + str(i) + ".bmp", rect)
                    # cv2.rectangle(frame, (x,y),(x+w,y+w),(0,255,0),2)
                images = dlib.get_face_chips(frame, faces, size=128)
                j = 0
                for image in images:
                    cv2.imwrite(dst_dir + "/" + prefix + "-" + str(i) + "-" + str(j) + ".bmp", image)
                    j += 1
        print(i)
        i += 1

    cap.release()
    cv2.destroyAllWindows()

# def detect_and_sub_image(src_path, dst_path_prefix, model_path):
#     img = cv2.imread(src_path)
#     dlib_face_detector = dlib.get_frontal_face_detector()
#     sp = dlib.shape_predictor(model_path)
#     dets = dlib_face_detector(img, 1)
#     faces = dlib.full_object_detections()
#     i = 0
#     if len(dets) != 0:
#         for detection in dets:
#             faces.append(sp(img, detection))
#             # rect = frame[det.top():det.bottom(), det.left():det.right()]
#             # rect = cv2.resize(rect, (128, 128))
#             # cv2.imwrite("E:/vscodeworkspace/facedata/data/dth06/dlib/" + str(i) + ".bmp", rect)
#             # cv2.rectangle(frame, (x,y),(x+w,y+w),(0,255,0),2)
#         images = dlib.get_face_chips(img, faces, size=128)
#         for image in images:
#             cv2.imwrite(dst_dir + "/" + prefix + "-" + str(i) + ".bmp", image)

detect_and_sub_video(0, "E:\\test", '9')
