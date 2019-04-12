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
 * @date 2019/4/11 14:51
 */
public class FreeTypeTest {
    static {
        System.load("D:/openCV/opencv/build/java/x64/opencv_java341.dll/");
    }
    public static void main(String[] args) {
        Mat m = Imgcodecs.imread("E:\\vscodeworkspace\\FaceRecognition\\userface\\jiji\\TIM20190412165226.jpg");
        CascadeClassifier cascadeClassifier = new CascadeClassifier("D:/openCV/opencv/sources/data/haarcascades/haarcascade_frontalface_alt.xml");
        MatOfRect matOfRect = new MatOfRect();
        cascadeClassifier.detectMultiScale(m, matOfRect);
        List<Rect> rects = matOfRect.toList();

        System.out.println(rects.size());

//        f("E:\\vscodeworkspace\\FaceRecognition\\userface\\train");
    }

    public static void f(String path) {
        File f = new File(path);
        if (f.isDirectory()) {
            String[] list = f.list();
            for (String s : list) {
                Mat imread = Imgcodecs.imread(path + "/" + s);
                List<Mat> dst = new ArrayList<>();
                Core.split(imread, dst);
                Imgproc.equalizeHist(dst.get(0), dst.get(0));
                Imgproc.equalizeHist(dst.get(1), dst.get(1));
                Imgproc.equalizeHist(dst.get(2), dst.get(2));
                Mat m = new Mat();
                Core.merge(dst, m);
                Imgcodecs.imwrite(path + "/histed" + s, m);
            }
        }
    }
}
