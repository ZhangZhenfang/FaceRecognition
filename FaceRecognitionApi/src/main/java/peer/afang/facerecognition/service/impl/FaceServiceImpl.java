package peer.afang.facerecognition.service.impl;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import peer.afang.facerecognition.mapper.FaceMapper;
import peer.afang.facerecognition.pojo.Face;
import peer.afang.facerecognition.property.Path;
import peer.afang.facerecognition.service.FaceService;

import javax.annotation.Resource;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 19:23
 */
@Service
public class FaceServiceImpl implements FaceService {

    private static final Logger LOGGER = LoggerFactory.getLogger(FaceServiceImpl.class);

    @Resource
    Path path;

    @Resource
    FaceMapper faceMapper;

    @Override
    public Face getByFaceId(Integer faceid) {
        return faceMapper.selectByPrimaryKey(faceid);
    }

    @Override
    public Integer addFace(Face face, String srcPath, List<String> facePaths) {
        String userFacePath = path.getUserFacePath();
        String tmpSrcDir = userFacePath + face.getUserid() + "/src/";
        String tmpFaceDir = userFacePath + face.getUserid() + "/face/";
        checkDir(tmpFaceDir);
        checkDir(tmpSrcDir);
        FileInputStream is;
        FileOutputStream os;
        try {
            face.setImagename("tmpname");
            faceMapper.insertSelective(face);
            LOGGER.info(face.toString());
            face.setImagename(face.getUserid() + "_" + face.getFaceid() + ".bmp");
            is = new FileInputStream(new File(srcPath));
            os = new FileOutputStream(new File(tmpSrcDir + face.getUserid() + "_" +
                    face.getFaceid() + ".bmp"));
            long l = 0;
            byte[] bytes = new byte[512];
            while ((l = is.read(bytes)) != -1) { os.write(bytes); }
            os.flush();
            if (null != is) { is.close(); }
            if (null != os) { os.close(); }
            for (String s : facePaths) {
                is = new FileInputStream(new File(s));
                os = new FileOutputStream(new File(tmpFaceDir + face.getImagename()));
                while ((l = is.read(bytes)) != -1) { os.write(bytes); }
            }
            os.flush();
            if (null != is) { is.close(); }
            if (null != os) { os.close(); }
        } catch (IOException e) {
            LOGGER.error("IO异常", e);
        }
        faceMapper.updateByPrimaryKey(face);
        return face.getFaceid();
    }

    @Override
    public List<Face> listByUserid(Integer userid) {
        return faceMapper.listByUserid(userid);
    }

    @Override
    public Integer countByUserid(Integer userid) {
        return faceMapper.countByUserid(userid);
    }

    private void checkDir(String path) {
        File d = new File(path);
        if (!d.exists()) {
            d.mkdirs();
        }
    }
}
