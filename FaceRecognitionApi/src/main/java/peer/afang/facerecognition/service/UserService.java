package peer.afang.facerecognition.service;

import peer.afang.facerecognition.pojo.User;

import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 19:18
 */
public interface UserService {

    /**
     * 通过userid获取user
     * @param userid
     * @return
     */
    User getById(Integer userid);

    /**
     * 添加user
     * @param user
     * @return
     */
    Integer addUser(User user);

    /**
     * 通过userName获取user
     * @param userName
     * @return
     */
    User getByName(String userName);

    /**
     * 获取所有的用户
     * @return
     */
    List<User> listAll();
}
