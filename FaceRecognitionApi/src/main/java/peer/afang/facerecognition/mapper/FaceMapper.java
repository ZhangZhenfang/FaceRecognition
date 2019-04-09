package peer.afang.facerecognition.mapper;

import peer.afang.facerecognition.pojo.Face;

import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/1 16:26
 */
public interface FaceMapper {
    /**
     * 根据主键删除
     * @param faceid
     * @return
     */
    int deleteByPrimaryKey(Integer faceid);

    /**
     * 插入一个face
     * @param record
     * @return
     */
    int insert(Face record);

    /**
     * 选择性的插入一个face
     * @param record
     * @return
     */
    int insertSelective(Face record);

    /**
     * 通过faceid查询face
     * @param faceid
     * @return
     */
    Face selectByPrimaryKey(Integer faceid);

    /**
     * 根据faceid选择性的更新face
     * @param record
     * @return
     */
    int updateByPrimaryKeySelective(Face record);

    /**
     * 根据faceid更新face
     * @param record
     * @return
     */
    int updateByPrimaryKey(Face record);

    /**
     * 查询userid的所有face
     * @param userid
     * @return
     */
    List<Face> listByUserid(Integer userid);
}