package peer.afang.facerecognition.util;

import com.alibaba.fastjson.JSONObject;

/**
 * @author ZhangZhenfang
 * @date 2019/4/9 15:13
 */

public class ResponseUtil {
    public static JSONObject wrapResponse(Object status, Object message, Object data) {
        JSONObject result = new JSONObject();
        result.put("status", status);
        result.put("message", message);
        result.put("data", data);
        return result;
    }
}
