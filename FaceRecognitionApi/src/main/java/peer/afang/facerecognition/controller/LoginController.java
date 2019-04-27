package peer.afang.facerecognition.controller;

import com.alibaba.fastjson.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import peer.afang.facerecognition.pojo.Account;
import peer.afang.facerecognition.service.AccountService;
import peer.afang.facerecognition.util.ResponseUtil;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

/**
 * @author ZhangZhenfang
 * @date 2019/4/27 19:29
 */
@Controller
@RequestMapping("/login")
public class LoginController {

    private Logger LOGGER = LoggerFactory.getLogger(LoginController.class);

    @Resource
    AccountService accountService;

    @ResponseBody
    @RequestMapping(value = "/login")
    public JSONObject login(@RequestParam(value = "account") String account,
                            @RequestParam(value = "password") String password,
                            HttpServletRequest request) {
        Account byAccount = accountService.getByAccount(account);
        if (byAccount == null) {
            return ResponseUtil.wrapResponse(2, "密码错误", "");
        }
        if (byAccount.getPassword().equals(password)) {
            HttpSession session = request.getSession();
            session.setAttribute("user", byAccount.getAccount());
            return ResponseUtil.wrapResponse(1, "success", "");
        } else {
            return ResponseUtil.wrapResponse(2, "密码错误", "");
        }
    }

    @ResponseBody
    @RequestMapping("/logout")
    public JSONObject logout(HttpServletRequest request) {
        HttpSession session = request.getSession();
        if (session != null) {
            session.removeAttribute("user");
        }
        return ResponseUtil.wrapResponse(1, "success", "");
    }

    @ResponseBody
    @RequestMapping("/getAccountInfo")
    public JSONObject getAccountInfo(HttpServletRequest request) {
        HttpSession session = request.getSession();
        String user = "account";
        if (session != null) {
            user = (String) session.getAttribute("user");
            return ResponseUtil.wrapResponse(1, "success", user);
        } else {
            return ResponseUtil.wrapResponse(2, "success", user);
        }
    }
}
