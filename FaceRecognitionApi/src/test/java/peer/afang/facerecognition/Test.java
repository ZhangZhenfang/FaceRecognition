package peer.afang.facerecognition;

import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;

import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/2 10:21
 */
public class Test {
    static {
        System.load("D:/openCV/opencv/build/java/x64/opencv_java341.dll");
    }
    public static String path = "E:/vscodeworkspace/FaceRecognition/src/main/resources/imgs/";
    public static String modelPath = "D:/openCV/opencv/sources/data/haarcascades/haarcascade_frontalface_alt.xml";

    public static void main(String[] args) {
        Mat imread = Imgcodecs.imread(path + "datahttp-nio-8080-exec-9.png");
        Mat dst = new Mat();
        Imgproc.resize(imread, dst, new Size(160, 120));
        System.out.println(imread);
        System.out.println(dst);
        long start = System.currentTimeMillis();
        CascadeClassifier cascadeClassifier = new CascadeClassifier(modelPath);
        MatOfRect matOfRect = new MatOfRect();
        cascadeClassifier.detectMultiScale(dst, matOfRect);
        System.out.println(System.currentTimeMillis() - start);
        List<Rect> rects = matOfRect.toList();
        for (Rect rect : rects) {
            System.out.println(rect.x + " " + rect.width + " " + rect.y + " " +rect.height);
            Imgproc.rectangle(dst, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height),
                    new Scalar(0, 255, 0));
        }
        Imgcodecs.imwrite(path + "tttt.png", dst);
        start = System.currentTimeMillis();
        matOfRect = new MatOfRect();
        cascadeClassifier.detectMultiScale(imread, matOfRect);
        System.out.println(System.currentTimeMillis() - start);
        rects = matOfRect.toList();
        for (Rect rect : rects) {
            System.out.println(rect.x + " " + rect.width + " " + rect.y + " " +rect.height);
            Imgproc.rectangle(imread, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y + rect.height),
                    new Scalar(0, 255, 0));
        }
        Imgcodecs.imwrite(path + "tttttttt.png", dst);
    }
}
