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
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;
import peer.afang.facerecognition.pojo.User;
import peer.afang.facerecognition.property.Path;
import peer.afang.facerecognition.property.Urls;
import peer.afang.facerecognition.service.UserService;
import peer.afang.facerecognition.util.*;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.*;

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
    private Urls urls;

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
            LOGGER.info("{}", strings);
            String s = HttpClientUtil.PostFiles(urls.getFace() + "/predict", strings, new HashMap<>());
            result.put("status", 1);
            result.put("message", "识别成功");
            result.put("data", s);
        } else if ("image".equals(type)) {
            strings = FaceDetectUtil.detectFaceAndSub(outPath);

            if (CollectionUtils.isEmpty(strings)) {
                result.put("status", 3);
                result.put("message", "图片中未检测到人脸");
            } else {
                String s = HttpClientUtil.PostFiles(urls.getFace() + "/predict", strings, new HashMap<>());
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
    @RequestMapping(value = "/detectPlus", method = {RequestMethod.POST, RequestMethod.GET})
    public String detectPlus(@RequestParam(value = "data") MultipartFile data) {
        Mat m = getMat(data);
        List<Rect> rects = detectFun(data, m);
        int i = 0;
        List<String> paths = new ArrayList<>();
        for (Rect rect : rects) {
            Mat submat = m.submat(rect.y, rect.y + rect.height, rect.x, rect.x + rect.width);
            Imgproc.resize(submat, submat, new Size(160, 160));
            Imgcodecs.imwrite(path.getTmpPath() + "/" + Thread.currentThread().getId() + "_" + i + ".png", submat);
            paths.add(path.getTmpPath() + "/" + Thread.currentThread().getId() + "_" + i++ + ".png");
            Imgproc.rectangle(m, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y +
                    rect.height), new Scalar(0, 255, 0));
        }
        for (String s : paths) {
            MatUtil.eHist(s, s);
        }
        HashMap<String, String> params = new HashMap<>(16);
        params.put("height", String.valueOf(160));
        params.put("width", String.valueOf(160));
        params.put("channel", String.valueOf(3));
        String s = HttpClientUtil.PostFiles(urls.getFace() + "/predict", paths, params);
        if (!StringUtils.isEmpty(s)) {
            String[] res = s.split(",");
            String substring1 = res[0].substring(1, res[0].length() - 1);
            String substring2 = res[1].substring(1, res[1].length() - 1);
            substring1 = substring1.trim();
            substring2 = substring2.trim();
            String[] split = substring1.split("\\s+");
            String[] ps = substring2.split("\\s+");
            i = 0;
            LOGGER.info("{}", Arrays.toString(split));
            for (Rect rect : rects) {
                User byId = userService.getById(Integer.parseInt(split[i++]) + 1);
                HashMap<String, String> p = new HashMap<>();
                p.put("text", byId == null ? "未知" : byId.getUsername());
//                p.put("text", byId == null ? "未知" : byId.getUsername() + ps[i - 1]);
                String post = HttpClientUtil.get(urls.getText2Mat() + "/text2Mat", p);
                if (post != null && post.length() > 3) {
                    byte[] decode = java.util.Base64.getDecoder().decode(post.substring(2, post.length() - 1));
                    Mat mat = Imgcodecs.imdecode(new MatOfByte(decode), Imgcodecs.CV_LOAD_IMAGE_UNCHANGED);
                    mat.convertTo(mat, m.type());
                    MatUtil.copy(mat, m, rect.x, rect.y);
                }
            }
        }
        MatOfByte matOfByte = new MatOfByte();
        Imgcodecs.imencode(".jpg", m, matOfByte);
        byte[] base64Bytes = Base64.encodeBase64(matOfByte.toArray());
        return new String(base64Bytes);
    }

    /**
     * 检测人脸并将结果返回
     * @param data
     * @return
     */
    @ResponseBody
    @RequestMapping(value = "/detect", method = {RequestMethod.POST, RequestMethod.GET})
    public String detect(@RequestParam(value = "data") MultipartFile data) {
        Mat m = getMat(data);
        List<Rect> rects = detectFun(data, m);
        int i = 0;
        for (Rect rect : rects) {
            Imgproc.rectangle(m, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y +
                    rect.height), new Scalar(0, 255, 0));
        }
        MatOfByte matOfByte = new MatOfByte();
        Imgcodecs.imencode(".png", m, matOfByte);
        byte[] base64Bytes = Base64.encodeBase64(matOfByte.toArray());
        return new String(base64Bytes);
    }

    @ResponseBody
    @RequestMapping(value = "/verify")
    public Boolean verify(@RequestParam(value = "data") MultipartFile data,
                          @RequestParam(value = "userName") String userName, HttpServletRequest request) {
        Mat m = getMat(data);
        List<Rect> rects = detectFun(data, m);
        LOGGER.info("{}", rects.size());
        if (rects.size() == 0 || rects.size() > 1) {
            return false;
        }
        int i = 0;
        List<String> paths = new ArrayList<>();
        Rect rect = rects.get(0);
        Mat submat = m.submat(rect.y, rect.y + rect.height, rect.x, rect.x + rect.width);
        Imgproc.resize(submat, submat, new Size(128, 128));
        Imgcodecs.imwrite(path.getTmpPath() + "/" + Thread.currentThread().getId() + "_" + i + ".png", submat);
        paths.add(path.getTmpPath() + "/" + Thread.currentThread().getId() + "_" + i++ + ".png");
        Imgproc.rectangle(m, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y +
                rect.height), new Scalar(0, 255, 0));

        for (String s : paths) {
            MatUtil.eHist(s, s);
        }
        HashMap<String, String> params = new HashMap<>(16);
        params.put("height", String.valueOf(128));
        params.put("width", String.valueOf(128));
        params.put("channel", String.valueOf(3));
        String s = HttpClientUtil.PostFiles(urls.getFace() + "/predict", paths, params);
        if (!StringUtils.isEmpty(s)) {
            String substring = s.substring(1, s.length() - 1);
            substring = substring.trim();
            String[] split = substring.split("\\s+");
            i = 0;
            LOGGER.info("{}", Arrays.toString(split));
            User byId = userService.getById(Integer.parseInt(split[i++]) + 1);
            if (byId != null) {
                if (byId.getUsername().equals(userName)) {
                    return true;
                }
            }
        }
        return false;
    }

    @ResponseBody
    @RequestMapping("fakeRealPlus")
    public String fakeRealPlus(@RequestParam(value = "data") MultipartFile data) {
        Mat m = getMat(data);
        List<Rect> rects = detectFun(data, m);
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
        HashMap<String, String> params = new HashMap<>(16);
        params.put("height", String.valueOf(128));
        params.put("width", String.valueOf(128));
        params.put("channel", String.valueOf(3));
        String s = HttpClientUtil.PostFiles(urls.getFakeReal() + "/predict", paths, params);
        if (!StringUtils.isEmpty(s)) {
            String substring = s.substring(1, s.length() - 1);
            substring = substring.trim();
            String[] split = substring.split("\\s+");
            i = 0;
            LOGGER.info("{}", Arrays.toString(split));
            for (Rect rect : rects) {
                HashMap<String, String> p = new HashMap<>();
                p.put("text", split[i++].equals("1") ? "REAL" : "FAKE");
                String post = HttpClientUtil.get(urls.getFace() + "/text2Mat", p);
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


    @ResponseBody
    @RequestMapping("fakeReal")
    public boolean fakeReal(@RequestParam(value = "data") MultipartFile data) {
        Mat m = getMat(data);
        List<Rect> rects = detectFun(data, m);
        LOGGER.info("{}", rects.size());
        if (rects.size() == 0 || rects.size() > 1) {
            return false;
        }
        int i = 0;
        List<String> paths = new ArrayList<>();
        Rect rect = rects.get(0);
        Mat submat = m.submat(rect.y, rect.y + rect.height, rect.x, rect.x + rect.width);
        Imgproc.resize(submat, submat, new Size(128, 128));
        Imgcodecs.imwrite(path.getTmpPath() + "/" + Thread.currentThread().getId() + "_" + i + ".png", submat);
        paths.add(path.getTmpPath() + "/" + Thread.currentThread().getId() + "_" + i++ + ".png");
        Imgproc.rectangle(m, new Point(rect.x, rect.y), new Point(rect.x + rect.width, rect.y +
                rect.height), new Scalar(0, 255, 0));
        HashMap<String, String> params = new HashMap<>(16);
        params.put("height", String.valueOf(128));
        params.put("width", String.valueOf(128));
        params.put("channel", String.valueOf(3));
        String s = HttpClientUtil.PostFiles(urls.getFakeReal() + "/predict", paths, params);
        if (!StringUtils.isEmpty(s)) {
            String substring = s.substring(1, s.length() - 1);
            substring = substring.trim();
            String[] split = substring.split("\\s+");
            i = 0;
            LOGGER.info("{}", Arrays.toString(split));
            return split[i++].equals("1") ? true : false;
        }
        return false;
    }

    @ResponseBody
    @RequestMapping(value = "restore", method = RequestMethod.GET)
    public JSONObject restore() {
        String s = HttpClientUtil.get(urls.getFace() + "/restore", new HashMap<>());
        if ("success".equals(s)) {
            return ResponseUtil.wrapResponse(1, "部署成功", "");
        }
        return ResponseUtil.wrapResponse(2, "部署失败", "");
    }

    private Mat getMat(MultipartFile data) {
        String tmpPath = path.getTmpPath() + data.getName() + Thread.currentThread().getName() + ".png";
        File f = new File(tmpPath);
        try (InputStream is = data.getInputStream(); FileOutputStream os = new FileOutputStream(f)) {
            long length;
            byte[] bytes = new byte[512];
            while ((length = is.read(bytes)) != -1) { os.write(bytes); }
        } catch (IOException e) {
            LOGGER.error("IO异常", e);
        }
        return Imgcodecs.imread(tmpPath);
    }

    private List<Rect> detectFun(MultipartFile data, Mat m) {
        if (this.cascadeClassifier == null) {
            loadDetector();
        }
        MatOfRect matOfRect = new MatOfRect();
        cascadeClassifier.detectMultiScale(m, matOfRect);
        List<Rect> rects = matOfRect.toList();
        return rects;
    }

    private synchronized void loadDetector() {
        if (this.cascadeClassifier == null) {
            cascadeClassifier = new CascadeClassifier(path.getOpencvCasPath());
        }
    }
}
