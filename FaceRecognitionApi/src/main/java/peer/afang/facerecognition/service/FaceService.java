package peer.afang.facerecognition.service;

import peer.afang.facerecognition.pojo.Face;

import java.util.List;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 19:22
 */
public interface FaceService {

    Face getBuFaceId(Integer faceid);

    Integer addFace(Face face, String srcPath, List<String> facePaths);
}
