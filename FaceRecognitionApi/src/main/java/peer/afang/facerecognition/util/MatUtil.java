package peer.afang.facerecognition.util;

import org.opencv.core.Mat;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

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
}
