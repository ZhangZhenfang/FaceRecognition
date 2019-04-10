package peer.afang.facerecognition.service;

import peer.afang.facerecognition.pojo.Face;
import peer.afang.facerecognition.vo.FaceVO;

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
    FaceVO addFace(Face face, String srcPath, List<String> facePaths);

    /**
     * 获取用户userid的所有face
     * @param userid
     * @return
     */
    List<FaceVO> listByUserid(Integer userid);

    /**
     * 根据用户id统计照片数量
     * @param userid
     * @return
     */
    Integer countByUserid(Integer userid);
}
