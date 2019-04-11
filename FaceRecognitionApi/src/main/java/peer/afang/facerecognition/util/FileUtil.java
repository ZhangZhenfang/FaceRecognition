package peer.afang.facerecognition.util;

import java.io.*;

/**
 * @author ZhangZhenfang
 * @date 2019/4/8 10:11
 */
public class FileUtil {

    public static void saveStream(InputStream is, String outPath) throws IOException {
        long l = 0;
        byte[] bytes = new byte[512];
        OutputStream os = new FileOutputStream(new File(outPath));
        while ((l = is.read(bytes)) != -1) { os.write(bytes); }
        is.close();
        os.close();
    }

    public static boolean deleteFileOnExit(String path) {
        File file = new File(path);
        if (file.exists() && file.isFile()) {
            file.delete();
        }
        return !file.exists();
    }
    public static boolean deleteDirOnExit(String path) {
        File file = new File(path);
        if (file.exists() && file.isDirectory()) {
            file.delete();
        }
        return !file.exists();
    }
}
