package peer.afang.facerecognition.property;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.PropertySource;
import org.springframework.stereotype.Component;

import java.util.HashSet;

/**
 * @author ZhangZhenfang
 * @date 2019/4/1 20:22
 */
@Component
@PropertySource("classpath:application.properties")
@ConfigurationProperties(prefix = "origin")
public class OriginControl {
    private int originControlType;
    private HashSet origins;

    public HashSet getOrigins() {
        return origins;
    }

    public void setOrigins(HashSet origins) {
        this.origins = origins;
    }

    public int getOriginControlType() {
        return originControlType;
    }

    public void setOriginControlType(int originControlType) {
        this.originControlType = originControlType;
    }
}
