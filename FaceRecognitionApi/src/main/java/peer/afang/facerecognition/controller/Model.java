package peer.afang.facerecognition.controller;

import org.apache.commons.io.IOUtils;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;
import org.tensorflow.*;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

/**
 * @author ZhangZhenfang
 * @date 2019/4/6 16:13
 */
public class Model {
    static {
        System.load("D:/openCV/opencv/build/java/x64/opencv_java341.dll");
    }
    public static void main(String[] args) throws IOException {

        SavedModelBundle serve = SavedModelBundle.load("E:\\vscodeworkspace\\FaceRecognition\\FaceRecognitionCore\\m1", "serve");
        Session session = new Session(serve.graph());

        float[][][] img = new float[112][92][3];

        String path = "E:\\faces\\other\\s41_2.bmp";
        Mat imread = Imgcodecs.imread(path);
        for (int i = 0; i < imread.height(); i++) {
            for (int j = 0; j < imread.width(); j++) {
                double[] doubles = imread.get(i, j);
                img[i][j][0] = (float) doubles[0] / 255;
                img[i][j][1] = (float) doubles[1] / 255;
                img[i][j][2] = (float) doubles[2] / 255;
            }
        }
        float[] label = new float[42];
        label[40] = 1;

        Operation operation1 = serve.graph().operation("y_max");
        Operation operation2 = serve.graph().operation("y_conv_max");

//        for (int i = 0; i < img.length; i++) {
//            for (int j = 0; j < img[i].length; j++) {
//                for (int k = 0; k < img[i][j].length; k++) {
//                    System.out.print(img[i][j][k] + " ");
//                }
//                System.out.print(",");
//            }
//            System.out.println();
//        }
//        System.out.println(imread.channels());
        Output output1 = new Output(operation1, 0);
        Output output2 = new Output(operation2, 0);

        session.runner().feed("x", Tensor.create(img))
                .feed("y_", Tensor.create(label))
                .feed("keep_prob", Tensor.create(1.0f))
                .fetch(output1)
                .fetch(output2)
                .run();
    }

}
