package peer.afang.facerecognition.util;

import java.io.File;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 21:06
 */
public class DirUtils {
    public static void checkDir(String dir) {
        File d = new File(dir);
        if (!d.exists()) {
            d.mkdirs();
        }
    }
}
