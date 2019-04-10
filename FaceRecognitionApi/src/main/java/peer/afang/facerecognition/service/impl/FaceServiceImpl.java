package peer.afang.facerecognition.service.impl;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import peer.afang.facerecognition.mapper.FaceMapper;
import peer.afang.facerecognition.pojo.Face;
import peer.afang.facerecognition.property.Path;
import peer.afang.facerecognition.service.FaceService;
import peer.afang.facerecognition.vo.FaceVO;

import javax.annotation.Resource;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
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
    public FaceVO addFace(Face face, String srcPath, List<String> facePaths) {
        String userFacePath = path.getUserFacePath();
        String tmpSrcDir = userFacePath + face.getUserid() + "/src/";
        String tmpFaceDir = userFacePath + face.getUserid() + "/face/";
        checkDir(tmpFaceDir);
        checkDir(tmpSrcDir);
        FileInputStream is;
        FileOutputStream os;
        try {
            face.setImagename("tmpname");
            face.setTime(new Date());
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
        FaceVO faceVO = new FaceVO();
        BeanUtils.copyProperties(face, faceVO);
        faceVO.setUrl("userface/" + face.getUserid() + "/src/" + face.getImagename());
        return faceVO;
    }

    @Override
    public List<FaceVO> listByUserid(Integer userid) {
        List<Face> faces = faceMapper.listByUserid(userid);
        List<FaceVO> result = new ArrayList<>();
        for (Face f : faces) {
            FaceVO faceVO = new FaceVO();
            BeanUtils.copyProperties(f, faceVO);
            faceVO.setUrl("userface/" + f.getUserid() + "/src/" + f.getImagename());
            result.add(faceVO);
        }
        return result;
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
