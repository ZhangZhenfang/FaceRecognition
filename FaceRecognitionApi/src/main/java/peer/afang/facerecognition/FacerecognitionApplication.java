package peer.afang.facerecognition;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@MapperScan(basePackages = {"peer.afang.facerecognition.mapper"})
public class FacerecognitionApplication {

    public static void main(String[] args) {
        SpringApplication.run(FacerecognitionApplication.class, args);
    }

}
