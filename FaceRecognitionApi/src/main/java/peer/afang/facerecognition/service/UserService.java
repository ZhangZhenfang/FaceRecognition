package peer.afang.facerecognition.service;

import org.springframework.stereotype.Service;
import peer.afang.facerecognition.mapper.UserMapper;
import peer.afang.facerecognition.pojo.User;

import javax.annotation.Resource;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 19:18
 */
public interface UserService {

    User getById(Integer userid);

    Integer addUser(User user);

    User getByName(String userName);
}
