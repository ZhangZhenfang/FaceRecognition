package peer.afang.facerecognition.mapper;

import peer.afang.facerecognition.pojo.User;

/**
 * @author ZhangZhenfang
 * @date 2019/4/1 00:00
 */
public interface UserMapper {
    /**
     * 删除user
     * @param userid
     * @return
     */
    int deleteByPrimaryKey(Integer userid);

    /**
     * 插入一个user
     * @param record
     * @return
     */
    int insert(User record);

    /**
     * 选择性的插入一个user
     * @param record
     * @return
     */
    int insertSelective(User record);

    /**
     * 根据userid查询user
     * @param userid
     * @return
     */
    User selectByPrimaryKey(Integer userid);

    /**
     * 选择性的更新
     * @param record
     * @return
     */
    int updateByPrimaryKeySelective(User record);

    /**
     * 更新user
     * @param record
     * @return
     */
    int updateByPrimaryKey(User record);

    /**
     * 根据userName查询user
     * @param userName
     * @return
     */
    User getByUserName(String userName);
}