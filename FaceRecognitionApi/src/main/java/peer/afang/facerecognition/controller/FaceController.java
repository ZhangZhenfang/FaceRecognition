package peer.afang.facerecognition.controller;

import com.alibaba.fastjson.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import peer.afang.facerecognition.pojo.Face;
import peer.afang.facerecognition.pojo.User;
import peer.afang.facerecognition.property.Path;
import peer.afang.facerecognition.service.FaceService;
import peer.afang.facerecognition.service.UserService;
import peer.afang.facerecognition.util.DirUtils;
import peer.afang.facerecognition.util.FaceDetectUtil;
import peer.afang.facerecognition.util.ResponseUtil;
import peer.afang.facerecognition.vo.FaceVO;

import javax.annotation.Resource;
import java.io.*;
import java.util.*;

/**
 * @author ZhangZhenfang
 * @date 2019/3/23 20:57
 */
@Controller
@RequestMapping("/face")
public class FaceController {

    private static final Logger LOGGER = LoggerFactory.getLogger(FaceController.class);

    @Resource
    private Path path;

    @Resource
    private UserService userService;

    @Resource
    private FaceService faceService;

    /**
     * 添加样本
     * @param data
     * @param userName
     */
    @ResponseBody
    @RequestMapping(value = "/addFace", method = RequestMethod.POST)
    public JSONObject addFace(MultipartFile data, String userName) {
        JSONObject result = new JSONObject();
        User byName = userService.getByName(userName);
        if (byName == null) {
            result.put("status", 2);
            result.put("message", "请先添加");
            return result;
        }
        InputStream inputStream = null;
        FileOutputStream os = null;
        String tmpDir = path.getTmpPath() + Thread.currentThread().getId() + "/";
        DirUtils.checkDir(tmpDir);
        String tmpPath = tmpDir + data.getOriginalFilename();
        try {
            inputStream = data.getInputStream();
            os = new FileOutputStream(new File(tmpPath));
            long l = 0;
            byte[] bytes = new byte[512];
            while ((l = inputStream.read(bytes)) != -1) { os.write(bytes); }

        } catch (IOException e) {
            LOGGER.error("IO异常", e);
        } finally {
            try {
                if (null != inputStream) { inputStream.close(); }
                if (null != os) { os.close(); }
            } catch (IOException e) { LOGGER.error("关闭流IO异常", e); }
        }

        List<String> strings = FaceDetectUtil.detectFaceAndSub(tmpPath);
        if (CollectionUtils.isEmpty(strings)) {
            result.put("status", 3);
            result.put("message", "未检测到人脸");
        } else if (strings.size() > 1){
            result.put("status", 4);
            result.put("message", "检测到多个人脸");
        } else {
            Face face = new Face();
            face.setUserid(byName.getUserid());
            FaceVO faceVO = faceService.addFace(face, tmpPath, strings);
            result.put("status", 1);
            result.put("message", "上传成功");
            result.put("data", faceVO);
        }
        deleteFiles(tmpDir);
        return result;
    }

    /**
     * 通过userid获取人脸图片
     * @param userid
     * @return
     */
    @ResponseBody
    @RequestMapping(value = "/listByUserid", method = RequestMethod.GET)
    public JSONObject listFacesByUserid(Integer userid) {
        List<FaceVO> faces = faceService.listByUserid(userid);
        return ResponseUtil.wrapResponse(1, "success", faces);
    }

    /**
     * 根据faceid删除人脸图片
     * @param faceid
     * @return
     */
    @ResponseBody
    @RequestMapping(value = "/face/{faceid}", method = RequestMethod.DELETE)
    public JSONObject deleteFace(@PathVariable(value = "faceid") Integer faceid) {
        LOGGER.info("delete {}", faceid);
        Integer integer = faceService.deleteFace(faceid);
        return ResponseUtil.wrapResponse(1, "删除成功", integer);
    }

    /**
     * 查询用户的照片数量
     * @param userid
     * @return
     */
    @ResponseBody
    @RequestMapping(value = "/countByUserid", method = RequestMethod.GET)
    public JSONObject countFacesByUserid(Integer userid) {
        Integer faces = faceService.countByUserid(userid);
        return ResponseUtil.wrapResponse(1, "success", faces);
    }

    /**
     * 删除dir目录下的所有文件
     * @param dir
     */
    private void deleteFiles(String dir) {
        File d = new File(dir);
        if (d.isDirectory()) {
            String[] list = d.list();
            for (String s : list) {
                LOGGER.info(s);
                File f = new File(dir + s);
                if (f.exists()) {
                    f.delete();
                }
            }
        }
    }
}
