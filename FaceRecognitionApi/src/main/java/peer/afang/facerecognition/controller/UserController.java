package peer.afang.facerecognition.controller;

import com.alibaba.fastjson.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import peer.afang.facerecognition.pojo.User;
import peer.afang.facerecognition.service.UserService;
import peer.afang.facerecognition.util.ResponseUtil;
import peer.afang.facerecognition.vo.UserInfoVO;

import javax.annotation.Resource;
import java.util.Date;
import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/9 12:34
 */
@Controller
@RequestMapping(value = "/user")
public class UserController {

    private static final Logger LOGGER = LoggerFactory.getLogger(UserController.class);

    @Resource
    private UserService userService;

    /**
     * 添加用户
     * @return
     */
    @ResponseBody
    @RequestMapping(value = "addUser", method = RequestMethod.POST)
    public JSONObject addUser(String userName) {
        JSONObject result = new JSONObject();
        User byName = userService.getByName(userName);
        if (byName != null) {
            result.put("status", 2);
            result.put("message", "用户已存在");
            return result;
        }
        User user = new User();
        user.setUsername(userName);
        user.setTime(new Date());
        userService.addUser(user);
        result.put("status", 1);
        result.put("message", "添加成功");
        result.put("data", user);
        return result;
    }

    /**
     * 更新用户
     * @return
     */
    @ResponseBody
    @RequestMapping(value = "updateUser", method = RequestMethod.POST)
    public JSONObject updateUser(@RequestParam(value = "userid") Integer userid,
                                 @RequestParam(value = "username") String userName) {
        User byName = userService.getByName(userName);
        if (byName != null) {
            return ResponseUtil.wrapResponse(2, "用户名已经存在", "");
        }
        User user = userService.getById(userid);
        user.setUsername(userName);
        userService.updateUser(user);
        return ResponseUtil.wrapResponse(1, "更新成功", user);
    }

    /**
     * 获取所有用户
     * @return
     */
    @ResponseBody
    @RequestMapping(value = "listAllUser", method = RequestMethod.POST)
    public JSONObject listAllUser(@RequestParam(value = "pageNumber") Integer pageNumber,
                                  @RequestParam(value = "pageSize") Integer pageSize) {
        LOGGER.info("{}, {}", pageNumber, pageSize);
        JSONObject result = new JSONObject();
        List<UserInfoVO> users = userService.listPage(pageNumber, pageSize);
        result.put("status", 1);
        result.put("message", "success");
        result.put("data", users);
        return result;
    }

    /**
     * 统计所有用户数量
     * @return
     */
    @ResponseBody
    @RequestMapping(value = "/countAllUser", method = RequestMethod.GET)
    public JSONObject countAllUser() {
        Long countAllUser = userService.countAll();
        return ResponseUtil.wrapResponse(1, "success", countAllUser);
    }
}
