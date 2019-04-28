package peer.afang.facerecognition.conf;

import com.alibaba.fastjson.JSONObject;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.concurrent.FutureCallback;
import org.apache.http.impl.nio.client.CloseableHttpAsyncClient;
import org.apache.http.impl.nio.client.HttpAsyncClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import peer.afang.facerecognition.pojo.TrainUpdate;
import peer.afang.facerecognition.property.Path;
import peer.afang.facerecognition.property.Urls;
import peer.afang.facerecognition.service.TrainUpdateService;
import peer.afang.facerecognition.service.UserService;
import peer.afang.facerecognition.util.MatUtil;
import peer.afang.facerecognition.util.ResponseUtil;

import javax.annotation.Resource;
import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * @author ZhangZhenfang
 * @date 2019/4/27 14:21
 */
@Component
@Configuration
@EnableScheduling
public class ModelUpdateTask {
    volatile public static boolean flag = false;
    Logger LOGGER = LoggerFactory.getLogger(ModelUpdateTask.class);
    @Resource
    private TrainUpdateService trainUpdateService;

    @Resource
    UserService userService;

    @Resource
    Path path;

    @Resource
    private Urls urls;


    Lock lock = new ReentrantLock();
    @Scheduled(cron = "0 0/2 * * * ? ")
    private void f() {
        LOGGER.info("{}{}", "ModelUpdateTask", ModelUpdateTask.flag);
        if (ModelUpdateTask.flag) {
            ModelUpdateTask.flag = false;
            TrainUpdate trainUpdate = trainUpdateService.getLast();
            if ("training".equals(trainUpdate.getStatus()) || "create".equals(trainUpdate.getStatus())) {
                return;
            }
            prepareData(true);
            trainUpdate = trainUpdateService.create();
            CloseableHttpAsyncClient httpclient = HttpAsyncClients.createDefault();
            httpclient.start();
            HttpPost httpPost = new HttpPost(urls.getModel() + "/update");
            List<NameValuePair> nvps = new ArrayList<>();
            nvps.add(new BasicNameValuePair("url", ""));
            nvps.add(new BasicNameValuePair("id", trainUpdate.getTrainupdateid().toString()));
            Long aLong = userService.countAll();
            nvps.add(new BasicNameValuePair("out_length", String.valueOf(aLong)));
            try {
                httpPost.setEntity(new UrlEncodedFormEntity(nvps));
                httpPost.setHeader("ID", String.valueOf(trainUpdate.getTrainupdateid()));
            } catch (UnsupportedEncodingException e) {
                LOGGER.error("{}", e);
            }
            httpclient.execute(httpPost, new FutureCallback<HttpResponse>() {
                private final Integer id = Integer.parseInt(httpPost.getHeaders("ID")[0].getValue());
                @Override
                public void completed(final HttpResponse response) {
                    LOGGER.info("{}", id);
                    try {
                        String content = EntityUtils.toString(response.getEntity(), "UTF-8");
                        LOGGER.info("{}", content);
                        if (content.startsWith("success")) {
                            String[] split = content.split("=");
                            Integer id = Integer.parseInt(split[1]);
                            trainUpdateService.success(id, split[2], split[3]);
                        } else {
                            trainUpdateService.failed(id, "tmp", "tmp");
                        }
                    } catch (IOException e) {
                        LOGGER.error("{}", e);
                    }
                }
                @Override
                public void failed(final Exception ex) {
                    System.out.println(httpPost.getRequestLine() + "->" + ex);
                    System.out.println(" callback thread id is : " + Thread.currentThread().getId());
                    trainUpdateService.failed(id, "tmp", "tmp");
                }
                @Override
                public void cancelled() {
                    System.out.println(httpPost.getRequestLine() + " cancelled");
                    System.out.println(" callback thread id is : " + Thread.currentThread().getId());
                    trainUpdateService.failed(id, "tmp", "tmp");
                }
            });
        }
    }

    public JSONObject prepareData(Boolean equalHist) {
        String srcDir = path.getUserFacePath();
        String outDir = path.getTrainPath();
        File src = new File(srcDir);
        File out = new File(outDir);
        if (!src.exists()) {
            return ResponseUtil.wrapResponse(2, "源文件夹不存在", "");
        }
        File[] files1 = out.listFiles();
        for (File f : files1) {
            if (f.exists()) {
                f.delete();
            }
        }
        LinkedList<File> files = new LinkedList<>();
        files.add(src);
        File f;
        while (!files.isEmpty()) {
            f = files.pop();
            if (f.isFile()){
                MatUtil.eHist(f.getAbsolutePath(), outDir + f.getName());
            } else if (f.isDirectory() && f.getName().endsWith("face") || isnumber(f.getName())) {
                for (File file : f.listFiles()) {
                    files.add(file);
                }
            }
        }
        return ResponseUtil.wrapResponse(1, "updatesuccess", "");
    }

    private boolean isnumber(String str) {
        for (int i = 0; i < str.length(); i++) {
            if (!Character.isDigit(str.charAt(i))) {
                return false;
            }
        }
        return true;
    }

}
