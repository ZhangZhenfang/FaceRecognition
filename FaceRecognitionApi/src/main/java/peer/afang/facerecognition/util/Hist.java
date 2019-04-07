package peer.afang.facerecognition.util;

import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import java.io.File;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 17:16
 */
public class Hist {

    public static void main(String[] args) {
        String dir = "E:\\faces\\color\\64";
        String dstDir = "E:\\faces\\color\\64hist";

        File d = new File(dir);
//        for ()


    }

    public static Mat hist(String path) {
        Mat imread = Imgcodecs.imread(path);
        return hist(imread);
    }

    public static Mat hist(Mat mat) {
        Mat res = new Mat();
        Imgproc.equalizeHist(mat, res);
        return res;
    }
}
