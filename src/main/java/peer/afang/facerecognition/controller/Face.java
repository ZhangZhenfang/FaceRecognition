package peer.afang.facerecognition.controller;

import org.apache.tomcat.util.codec.binary.Base64;
import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import peer.afang.facerecognition.property.Path;

import javax.annotation.Resource;
import java.io.*;
import java.util.*;

/**
 * @author ZhangZhenfang
 * @date 2019/3/23 20:57
 */
@Controller
@RequestMapping("/face")
public class Face {

    private static final Logger LOGGER = LoggerFactory.getLogger(Face.class);

    @Resource
    private Path path;

    /**
     * 检测人脸并将结果返回
     * @param data
     * @return
     */
    @ResponseBody
    @RequestMapping(value = "/detect", method = RequestMethod.POST)
    public String detect(MultipartFile data) {
        if (data == null) {
            return "";
        }
        String tmpPath = path.getTmpPath() + data.getName() + Thread.currentThread().getName() + ".png";
        File f = new File(tmpPath);
        try (InputStream is = data.getInputStream(); FileOutputStream os = new FileOutputStream(f)) {
            long length;
            byte[] bytes = new byte[512];
            while ((length = is.read(bytes)) != -1) { os.write(bytes); }
        } catch (IOException e) {
            LOGGER.error("IO异常", e);
        }

        Mat m = Imgcodecs.imread(tmpPath);
        CascadeClassifier cascadeClassifier = new CascadeClassifier(path.getOpencvCasPath());
        MatOfRect matOfRect = new MatOfRect();
        cascadeClassifier.detectMultiScale(m, matOfRect);
        List<Rect> rects = matOfRect.toList();
        for (Rect rect : rects) {
            Imgproc.rectangle(m, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y +
                    rect.height), new Scalar(0, 255, 0));
        }
        MatOfByte matOfByte = new MatOfByte();
        Imgcodecs.imencode(".png", m, matOfByte);
        byte[] base64Bytes = Base64.encodeBase64(matOfByte.toArray());
        return new String(base64Bytes);
    }

    /**
     * 添加样本
     * @param data
     * @param name
     */
    @ResponseBody
    @RequestMapping(value = "/addSample", method = RequestMethod.POST)
    public void addSample(MultipartFile data, String name) {
    }
}
