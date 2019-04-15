package peer.afang.facerecognition.controller;

import com.alibaba.fastjson.JSONObject;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import peer.afang.facerecognition.pojo.TrainUpdate;
import peer.afang.facerecognition.service.TrainUpdateService;
import peer.afang.facerecognition.util.ResponseUtil;

import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/13 17:21
 */
@Controller
@RequestMapping("status")
public class StatusController {

    private List<String> steps = new ArrayList<>();
    
    @Resource
    TrainUpdateService trainUpdateService;

    @ResponseBody
    @RequestMapping("handler")
    public void handler(String id, String step) {
        steps.add(step);
    }

    @ResponseBody
    @RequestMapping("getSteps")
    public JSONObject getSteps(@RequestParam(value = "trainupdateid") Integer trainupdateid) {
        TrainUpdate trainUpdate = trainUpdateService.getById(trainupdateid);
        if ("success".equals(trainUpdate.getStatus()) || "failed".equals(trainUpdate.getStatus())) {
            steps.clear();
            return ResponseUtil.wrapResponse(1, "stop", steps);
        }
        return ResponseUtil.wrapResponse(1, "continue", steps);
    }
}
