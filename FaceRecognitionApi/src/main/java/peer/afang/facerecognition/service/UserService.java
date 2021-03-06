package peer.afang.facerecognition.service;

import peer.afang.facerecognition.pojo.User;
import peer.afang.facerecognition.vo.UserInfoVO;

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

    /**
     * 统计所有用户个数
     * @return
     */
    Long countAll();

    /**
     * 分页查询user
     * @param pageNumber
     * @param pageSize
     * @return
     */
    List<UserInfoVO> listPage(Integer pageNumber, Integer pageSize);

    /**
     * 更新用户信息
     * @param user
     */
    Integer updateUser(User user);

}
