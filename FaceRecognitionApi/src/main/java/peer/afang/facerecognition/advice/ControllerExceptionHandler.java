package peer.afang.facerecognition.advice;

import com.alibaba.fastjson.JSONObject;
import org.apache.tomcat.util.http.fileupload.FileUploadBase;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import peer.afang.facerecognition.util.ResponseUtil;

/**
 * @author ZhangZhenfang
 * @date 2019/4/10 16:24
 */
@ControllerAdvice
public class ControllerExceptionHandler {

    @ResponseBody
    @ExceptionHandler(FileUploadBase.SizeLimitExceededException.class)
    public JSONObject handlSizeLimitExceededException(FileUploadBase.SizeLimitExceededException e) {
        return ResponseUtil.wrapResponse(-1, "文件大小超限", "");
    }
}
