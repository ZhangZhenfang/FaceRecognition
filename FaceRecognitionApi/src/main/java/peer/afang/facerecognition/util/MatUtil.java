package peer.afang.facerecognition.util;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/11 18:35
 */
public class MatUtil {

    private static final Logger LOGGER = LoggerFactory.getLogger(MatUtil.class);

    public static void copy(Mat from, Mat to, int x, int y) {
        for (int i = 0; i < from.height(); i++) {
            for (int j = 0; j < from.width(); j++) {
                if (y + i < to.height() && x + j < to.width()) {
                    to.put(y + i, x + j, from.get(i, j));
                }
            }
        }
    }

    public static void eHist(String srcPath, String outPath) {
//        LOGGER.info("{}\n{}", srcPath, outPath);
        Mat imread = Imgcodecs.imread(srcPath);
        List<Mat> dst = new ArrayList<>();
        Core.split(imread, dst);
        Imgproc.equalizeHist(dst.get(0), dst.get(0));
        Imgproc.equalizeHist(dst.get(1), dst.get(1));
        Imgproc.equalizeHist(dst.get(2), dst.get(2));
        Mat m = new Mat();
        Core.merge(dst, m);
        Imgcodecs.imwrite(outPath, m);
    }
}
