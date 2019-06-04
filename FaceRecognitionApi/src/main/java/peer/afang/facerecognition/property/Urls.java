package peer.afang.facerecognition.property;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.PropertySource;
import org.springframework.stereotype.Component;

/**
 * @author ZhangZhenfang
 * @date 2019/4/21 13:13
 */
@Component
@PropertySource("classpath:application-dev.properties")
@ConfigurationProperties(prefix = "url")
public class Urls {

    private String face;
    private String text2Mat;
    private String model;
    private String fakeReal;

    public String getFace() {
        return face;
    }

    public String getText2Mat() {
        return text2Mat;
    }

    public void setText2Mat(String text2Mat) {
        this.text2Mat = text2Mat;
    }

    public void setFace(String face) {
        this.face = face;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public String getFakeReal() {
        return fakeReal;
    }

    public void setFakeReal(String fakeReal) {
        this.fakeReal = fakeReal;
    }
}
