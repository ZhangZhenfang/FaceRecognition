package peer.afang.facerecognition.service.impl;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import peer.afang.facerecognition.mapper.TrainUpdateMapper;
import peer.afang.facerecognition.pojo.TrainUpdate;
import peer.afang.facerecognition.service.TrainUpdateService;

import javax.annotation.Resource;
import java.util.Date;

/**
 * @author ZhangZhenfang
 * @date 2019/4/13 14:57
 */
@Service
public class TrainUpdateServiceImpl implements TrainUpdateService {
    private static final Logger LOGGER = LoggerFactory.getLogger(TrainUpdateServiceImpl.class);
    @Resource
    TrainUpdateMapper trainUpdateMapper;

    @Override
    public TrainUpdate getLast() {
        return trainUpdateMapper.getLast();
    }

    @Override
    public TrainUpdate create() {
        TrainUpdate trainUpdate = new TrainUpdate();
        trainUpdate.setStatus("create");
        trainUpdate.setTime(new Date());
        trainUpdate.setLog("tmp");
        trainUpdate.setParam("tmp");
        trainUpdate.setVersion("tmp");
        trainUpdateMapper.insert(trainUpdate);
        return trainUpdate;
    }

    @Override
    public void success(Integer id, String version, String log) {
        TrainUpdate byId = trainUpdateMapper.getById(id);
        byId.setVersion(version);
        byId.setLog(log);
        byId.setStatus("success");
        LOGGER.info("update {}", byId.toString());
        trainUpdateMapper.updateById(byId);
    }

    @Override
    public TrainUpdate getById(Integer trainupdateid) {
        return trainUpdateMapper.getById(trainupdateid);
    }

    @Override
    public void failed(Integer id, String tmp, String tmp1) {
        TrainUpdate byId = trainUpdateMapper.getById(id);
        byId.setVersion(tmp);
        byId.setLog(tmp1);
        byId.setStatus("failed");
        LOGGER.info("update {}", byId.toString());
        trainUpdateMapper.updateById(byId);
    }
}
