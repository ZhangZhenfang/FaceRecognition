package peer.afang.facerecognition.util;

import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 19:48
 */
@Component
public class FaceDetectUtil {
    private static final Logger LOGGER = LoggerFactory.getLogger(FaceDetectUtil.class);

    private static String CAS_PATH;
    private static String EYE_XML;

    @Value("${path.opencvCasPath}")
    public void setPath(String path) {
        FaceDetectUtil.CAS_PATH = path;
    }

    @Value("${path.eyexml}")
    public void setEyeXml(String path) {
        FaceDetectUtil.EYE_XML = path;
    }
    public static List<String> detectFaceAndSub(String path) {
        Mat srcMat = Imgcodecs.imread(path);
        CascadeClassifier cascadeClassifier = new CascadeClassifier(CAS_PATH);
        MatOfRect matOfRect = new MatOfRect();
        cascadeClassifier.detectMultiScale(srcMat, matOfRect);
        List<Rect> rects = matOfRect.toList();
        int i = 0;
        List<String> result = new ArrayList<>();
        LOGGER.info(path + "detect " + rects.size());
        for (Rect rect : rects) {
            Mat submat = srcMat.submat(rect.y, rect.y + rect.height, rect.x, rect.x + rect.width);
            if (detectEye(submat)) {
                Imgproc.resize(submat, submat, new Size(128, 128));
                String s = path + "_" + i + ".bmp";
                Imgcodecs.imwrite(s, submat);
                result.add(s);
            }
        }
        return result;
    }

    public static boolean detectEye(Mat srcMat) {
        CascadeClassifier cascadeClassifier = new CascadeClassifier(EYE_XML);
        MatOfRect matOfRect = new MatOfRect();
        cascadeClassifier.detectMultiScale(srcMat, matOfRect);
        List<Rect> rects = matOfRect.toList();
        LOGGER.info("{}", rects.size());
        return rects.size() >= 1 ? true : false;
    }
}
