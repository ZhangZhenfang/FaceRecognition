package peer.afang.facerecognition.controller;

import com.alibaba.fastjson.JSONObject;
import org.apache.tomcat.util.codec.binary.Base64;
import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.objdetect.CascadeClassifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import peer.afang.facerecognition.pojo.User;
import peer.afang.facerecognition.property.Path;
import peer.afang.facerecognition.service.UserService;
import peer.afang.facerecognition.util.FaceDetectUtil;
import peer.afang.facerecognition.util.FileUtil;
import peer.afang.facerecognition.util.HttpClientUtil;
import peer.afang.facerecognition.util.MatUtil;

import javax.annotation.Resource;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/9 15:01
 */
@Controller
@RequestMapping(value = "/model")
public class ModelController {

    private static final Logger LOGGER = LoggerFactory.getLogger(ModelController.class);

    private CascadeClassifier cascadeClassifier;
    @Resource
    private Path path;

    @Resource
    private UserService userService;

    /**
     * 识别人脸
     * @param data
     * @param type
     * @return
     */
    @ResponseBody
    @RequestMapping(value = "/recognize", method = RequestMethod.POST)
    public JSONObject recognize(MultipartFile data, String type) {
        JSONObject result = new JSONObject();
        if (type == null) {
            result.put("status", 2);
            result.put("message", "type不能为空");
            return result;
        }
        String tmpPath = path.getTmpPath() + Thread.currentThread().getId();
        String outPath = tmpPath + "/" + data.getOriginalFilename();
        try {
            FileUtil.saveStream(data.getInputStream(), outPath);
        } catch (IOException e) {
            LOGGER.error("IO异常", e);
        }
        List<String> strings;
        if ("face".equals(type)) {
            strings = new ArrayList<>();
            strings.add(outPath);
            String s = HttpClientUtil.PostFiles("http://localhost:12580/upload", strings, new HashMap<>());
            result.put("status", 1);
            result.put("message", "识别成功");
        } else if ("image".equals(type)) {
            strings = FaceDetectUtil.detectFaceAndSub(outPath);

            if (CollectionUtils.isEmpty(strings)) {
                result.put("status", 3);
                result.put("message", "图片中未检测到人脸");
            } else {
                String s = HttpClientUtil.PostFiles("http://localhost:12580/upload", strings, new HashMap<>());
                result.put("status", 1);
                result.put("message", "识别成功");
                result.put("data", s);
            }
        } else {
            result.put("status", 4);
            result.put("message", "类型错误");
        }
        return result;
    }

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
        if (this.cascadeClassifier == null) {
            loadDetector();
        }
        MatOfRect matOfRect = new MatOfRect();
        cascadeClassifier.detectMultiScale(m, matOfRect);
        List<Rect> rects = matOfRect.toList();
        int i = 0;
        List<String> paths = new ArrayList<>();
        for (Rect rect : rects) {
            Mat submat = m.submat(rect.y, rect.y + rect.height, rect.x, rect.x + rect.width);
            Imgproc.resize(submat, submat, new Size(128, 128));
            Imgcodecs.imwrite(path.getTmpPath() + "/" + Thread.currentThread().getId() + "_" + i + ".png", submat);
            paths.add(path.getTmpPath() + "/" + Thread.currentThread().getId() + "_" + i++ + ".png");
            Imgproc.rectangle(m, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y +
                    rect.height), new Scalar(0, 255, 0));
        }
        String s = HttpClientUtil.PostFiles("http://localhost:12580/upload", paths, new HashMap<>(16));
        if (s != null) {
            String substring = s.substring(1, s.length() - 1);
            String[] split = substring.split(" ");
            i = 0;
            for (Rect rect : rects) {
                User byId = userService.getById(Integer.parseInt(split[i++]) + 1);
                HashMap<String, String> p = new HashMap<>();
                p.put("text", byId.getUsername());
                String post = HttpClientUtil.get("http://localhost:12580/text2Mat", p);
                if (post != null && post.length() > 3) {
                    byte[] decode = java.util.Base64.getDecoder().decode(post.substring(2, post.length() - 1));
                    Mat mat = Imgcodecs.imdecode(new MatOfByte(decode), Imgcodecs.CV_LOAD_IMAGE_UNCHANGED);
                    mat.convertTo(mat, m.type());
                    MatUtil.copy(mat, m, rect.x, rect.y);
                }
            }
        }
        MatOfByte matOfByte = new MatOfByte();
        Imgcodecs.imencode(".png", m, matOfByte);
        byte[] base64Bytes = Base64.encodeBase64(matOfByte.toArray());
        return new String(base64Bytes);
    }

    private synchronized void loadDetector() {
        if (this.cascadeClassifier == null) {
            cascadeClassifier = new CascadeClassifier(path.getOpencvCasPath());
        }
    }
}
