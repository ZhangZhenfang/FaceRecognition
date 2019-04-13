package peer.afang.facerecognition.service;

import peer.afang.facerecognition.pojo.TrainUpdate;

/**
 * @author ZhangZhenfang
 * @date 2019/4/13 14:58
 */
public interface TrainUpdateService {
    TrainUpdate getLast();

    TrainUpdate create();

    void success(Integer id, String version, String log);

    TrainUpdate getById(Integer trainupdateid);

    void failed(Integer id, String tmp, String tmp1);
}
