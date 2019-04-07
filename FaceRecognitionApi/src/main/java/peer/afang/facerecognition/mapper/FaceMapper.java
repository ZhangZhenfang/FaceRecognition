package peer.afang.facerecognition.mapper;

import peer.afang.facerecognition.pojo.Face;

public interface FaceMapper {
    int deleteByPrimaryKey(Integer faceid);

    int insert(Face record);

    int insertSelective(Face record);

    Face selectByPrimaryKey(Integer faceid);

    int updateByPrimaryKeySelective(Face record);

    int updateByPrimaryKey(Face record);
}