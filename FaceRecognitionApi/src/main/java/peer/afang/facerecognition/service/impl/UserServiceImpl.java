package peer.afang.facerecognition.service.impl;

import org.springframework.stereotype.Service;
import peer.afang.facerecognition.mapper.UserMapper;
import peer.afang.facerecognition.pojo.User;
import peer.afang.facerecognition.service.UserService;

import javax.annotation.Resource;
import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 19:19
 */
@Service
public class UserServiceImpl implements UserService {

    @Resource
    UserMapper userMapper;

    @Override
    public User getById(Integer userid) {
        User user = userMapper.selectByPrimaryKey(userid);
        return user;
    }

    @Override
    public Integer addUser(User user) {
        int insert = userMapper.insert(user);
        return insert;
    }

    @Override
    public User getByName(String userName) {
        return userMapper.getByUserName(userName);
    }

    @Override
    public List<User> listAll() {
        return userMapper.listAll();
    }
}
