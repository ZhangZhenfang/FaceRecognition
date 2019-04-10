package peer.afang.facerecognition.service.impl;

import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import peer.afang.facerecognition.mapper.FaceMapper;
import peer.afang.facerecognition.mapper.UserMapper;
import peer.afang.facerecognition.pojo.User;
import peer.afang.facerecognition.service.UserService;
import peer.afang.facerecognition.vo.UserInfoVO;

import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 19:19
 */
@Service
public class UserServiceImpl implements UserService {

    @Resource
    UserMapper userMapper;
    @Resource
    FaceMapper faceMapper;

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

    @Override
    public Long countAll() {
        return userMapper.countAll();
    }

    @Override
    public List<UserInfoVO> listPage(Integer pageNumber, Integer pageSize) {
        Integer start = (pageNumber - 1) * pageSize;
        Integer end = start + pageSize;
        List<User> users = userMapper.listPage(start, end);
        List<UserInfoVO> result = new ArrayList<>();
        for (User user : users) {
            UserInfoVO userInfoVO = new UserInfoVO();
            Integer faces = faceMapper.countByUserid(user.getUserid());
            BeanUtils.copyProperties(user, userInfoVO);
            userInfoVO.setFaces(faces);
            result.add(userInfoVO);
        }
        return result;
    }

    @Override
    public Integer updateUser(User user) {
        return userMapper.updateByPrimaryKey(user);
    }
}
