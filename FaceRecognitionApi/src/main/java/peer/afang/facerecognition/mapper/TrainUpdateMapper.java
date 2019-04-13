package peer.afang.facerecognition.mapper;

import peer.afang.facerecognition.pojo.TrainUpdate;

import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/13 14:46
 */
public interface TrainUpdateMapper {

    TrainUpdate getById(Integer trainupdateid);
    Integer insert(TrainUpdate trainupdateid);
    Integer deleteById(Integer trainupdateid);
    Integer updateById(TrainUpdate trainUpdate);
    List<TrainUpdate> listAll();

    TrainUpdate getLast();

}
