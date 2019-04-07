package peer.afang.facerecognition.util;

import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.io.File;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 17:16
 */
public class Hist {
    static {
        System.load("D:/openCV/opencv/build/java/x64/opencv_java341.dll");
    }
    public static void main(String[] args) {
        String dirtest = "E:\\faces\\color\\64\\colortest";
        String dirtrain = "E:\\faces\\color\\64\\colortrain";
        String dstTest = "E:\\faces\\color\\64hist\\colortest";
        String dstDir = "E:\\faces\\color\\64hist\\colortrain";

        hist(dirtrain, dstDir);
    }
    public static void hist(String src, String dst) {
        File srcDir = new File(src);
        String[] list = srcDir.list();
        for (String s : list) {
            Mat imread = Imgcodecs.imread(src + "/" + s, Imgcodecs.CV_LOAD_IMAGE_GRAYSCALE);
//            imread.convertTo(imread, CvType.CV_32FC1);
            Imgproc.equalizeHist(imread, imread);
            Imgcodecs.imwrite(dst + "/" + s, imread);
        }
    }
}
