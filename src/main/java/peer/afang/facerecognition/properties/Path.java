package peer.afang.facerecognition.properties;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.PropertySource;
import org.springframework.stereotype.Component;

/**
 * @author ZhangZhenfang
 * @date 2019/4/1 16:26
 */
@Component
@PropertySource("classpath:application.properties")
@ConfigurationProperties(prefix = "path")
public class Path {
    private String tmpPath;
    private String opencvPath;
    private String opencvCasPath;
    public String getTmpPath() {
        return tmpPath;
    }

    public void setTmpPath(String tmpPath) {
        this.tmpPath = tmpPath;
    }

    public String getOpencvPath() {
        return opencvPath;
    }

    public void setOpencvPath(String opencvPath) {
        this.opencvPath = opencvPath;
    }

    public String getOpencvCasPath() {
        return opencvCasPath;
    }

    public void setOpencvCasPath(String opencvCasPath) {
        this.opencvCasPath = opencvCasPath;
    }
}
