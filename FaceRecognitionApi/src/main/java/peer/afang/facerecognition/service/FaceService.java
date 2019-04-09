package peer.afang.facerecognition.service;

import peer.afang.facerecognition.pojo.Face;

import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 19:22
 */
public interface FaceService {

    /**
     * 通过faceid查询face
     * @param faceid
     * @return
     */
    Face getByFaceId(Integer faceid);

    /**
     * 添加face
     * @param face
     * @param srcPath
     * @param facePaths
     * @return
     */
    Integer addFace(Face face, String srcPath, List<String> facePaths);
}
