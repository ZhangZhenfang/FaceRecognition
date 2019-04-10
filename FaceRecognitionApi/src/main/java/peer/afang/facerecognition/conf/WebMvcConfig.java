package peer.afang.facerecognition.conf;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import peer.afang.facerecognition.property.Path;

import javax.annotation.Resource;

/**
 * @author ZhangZhenfang
 * @date 2019/4/10 17:25
 */
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {
    @Resource
    private Path path;
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/userface/**").addResourceLocations("file:" + path.getUserFacePath());
    }
}
