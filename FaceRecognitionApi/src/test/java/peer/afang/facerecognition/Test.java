package peer.afang.facerecognition;

import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/2 10:21
 */
public class Test {
    static {
        System.load("D:/openCV/opencv/build/java/x64/opencv_java341.dll");
    }
    public static String path = "E:\\faces\\colortrain\\000";
    public static String modelPath = "D:/openCV/opencv/sources/data/haarcascades/haarcascade_frontalface_alt.xml";

    public static void main(String[] args) {
//        Mat imread = Imgcodecs.imread("E:\\faces\\color\\source0-99\\003\\003_4.bmp");
//        System.out.println(imread);
//        List<Mat> detect = detect(imread);
//        System.out.println(detect.size());
//        int i= 0;
//        for (Mat m : detect) {
//            Imgcodecs.imwrite("E:\\faces\\color\\source0-99\\003\\" + i++ + ".bmp", m);
//        }
        resize64();
//        dataSet();
//        Mat imread = Imgcodecs.imread(path + "/000_0.bmp");
//        System.out.println(imread);
//        List<Mat> detects = detect(imread);
//        Imgcodecs.imwrite(path + "/000_0_0.bmp", imread);
//        for (Mat mat : detects) {
//            Imgcodecs.imwrite(path + "/000_0_1.bmp", mat);
//        }
    }
    public static void dataSet() {
        String path = "E:\\faces\\color\\source200-299";
        String trainPath = "E:\\faces\\color\\colortrain200-299";
        String testPath = "E:\\faces\\color\\colortest200-299";
        visit(path, trainPath, testPath);
    }

    public static void visit(String path, String trainPath, String testPath) {
        File file = new File(path);
        if (file.isDirectory()) {
            String[] list = file.list();
            for (String s : list) {
                visit(path + "/" + s, trainPath, testPath);
            }
        } else if (file.isFile()){
            System.out.println(file.getName());
            Mat imread = Imgcodecs.imread(file.getAbsolutePath());
            List<Mat> detect = detect(imread);
            String[] s = file.getName().split("_");
            System.out.println(s[1]);
            String newName = Integer.parseInt(s[0]) + "_" + s[1];
            if (s[1].startsWith("4")) {
                if (!detect.isEmpty()) {
                    if (detect.size() == 1) {
                        Imgcodecs.imwrite(testPath + "/" + newName, detect.get(0));
                    } else {
                        for (int i = 0; i < detect.size(); i++) {
                            Imgcodecs.imwrite(testPath + "/" + Integer.parseInt(s[0]) + "_" + i + "_" + s[1], detect.get(i));
                        }
                    }

                }
            } else {
                if (!detect.isEmpty()) {
                    if (detect.size() == 1) {
                        Imgcodecs.imwrite(trainPath + "/" + newName, detect.get(0));
                    } else {
                        for (int i = 0; i < detect.size(); i++) {
                            Imgcodecs.imwrite(trainPath + "/" + Integer.parseInt(s[0]) + "_" + i + "_" + s[1], detect.get(i));
                        }
                    }
                }
            }
        }
    }

    public static List<Mat> detect(Mat image) {
        List<Mat> result = new ArrayList<>();
        CascadeClassifier cascadeClassifier = new CascadeClassifier(modelPath);
        MatOfRect matOfRect = new MatOfRect();
        cascadeClassifier.detectMultiScale(image, matOfRect);
        List<Rect> rects = matOfRect.toList();
        for (Rect rect : rects) {
            Mat m = new Mat();
            Imgproc.resize(image.submat(rect), m, new Size(128, 128));
            result.add(m);
        }
        return result;
    }

    public static void test() {
        String path = "E:\\faces\\color\\colortest\\192_4.png";
        String out = "E:\\faces\\color\\colortest\\192_4.bmp";
        Mat imread = Imgcodecs.imread(path);
        System.out.println(imread);
        Imgcodecs.imwrite(out, imread);
    }

    public static void resize64() {
        String trainpath = "E:\\faces\\color\\colortrain";
        String testpath = "E:\\faces\\color\\colortest";
        String train = "E:\\faces\\color\\64\\colortrain";
        String test = "E:\\faces\\color\\64\\colortest";

        File f = new File(trainpath);
        String[] list = f.list();
        for (String s : list) {
            Mat imread = Imgcodecs.imread(trainpath + "/" + s);
            Mat dst = new Mat();
            Imgproc.resize(imread, dst, new Size(64, 64));
            Imgcodecs.imwrite(train + "/" + s, dst);
        }
        f = new File(testpath);
        list = f.list();
        for (String s : list) {
            Mat imread = Imgcodecs.imread(testpath + "/" + s);
            Mat dst = new Mat();
            Imgproc.resize(imread, dst, new Size(64, 64));
            Imgcodecs.imwrite(test + "/" + s, dst);
        }
    }
}
