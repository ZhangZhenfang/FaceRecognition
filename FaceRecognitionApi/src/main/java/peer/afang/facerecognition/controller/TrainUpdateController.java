package peer.afang.facerecognition.controller;

import com.alibaba.fastjson.JSONObject;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.concurrent.FutureCallback;
import org.apache.http.impl.nio.client.CloseableHttpAsyncClient;
import org.apache.http.impl.nio.client.HttpAsyncClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import peer.afang.facerecognition.pojo.TrainUpdate;
import peer.afang.facerecognition.property.Path;
import peer.afang.facerecognition.service.TrainUpdateService;
import peer.afang.facerecognition.service.impl.TrainUpdateServiceImpl;
import peer.afang.facerecognition.util.HttpClientUtil;
import peer.afang.facerecognition.util.MatUtil;
import peer.afang.facerecognition.util.ResponseUtil;

import javax.annotation.Resource;
import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.*;

/**
 * @author ZhangZhenfang
 * @date 2019/4/13 14:59
 */
@Controller
@RequestMapping("/trainupdate")
public class TrainUpdateController {

    private static final Logger LOGGER = LoggerFactory.getLogger(TrainUpdateController.class);

    @Resource
    TrainUpdateService trainUpdateService;

    @Resource
    Path path;

    @ResponseBody
    @RequestMapping(value = "trainModel")
    public JSONObject train() {
        HashMap<String, String> p = new HashMap<>();
        p.put("batch_size", "20");
        String post = HttpClientUtil.post("http://localhost:12580/train", p);

        return ResponseUtil.wrapResponse(1, "trainsuccess", post);
    }

    @ResponseBody
    @RequestMapping(value = "update")
    public JSONObject updateModel() {
        TrainUpdate trainUpdate = trainUpdateService.getLast();
        if ("training".equals(trainUpdate.getStatus()) || "create".equals(trainUpdate.getStatus())) {
            return ResponseUtil.wrapResponse(1, "training||create", trainUpdate);
        }
        prepareData(true);
        trainUpdate = trainUpdateService.create();
        CloseableHttpAsyncClient httpclient = HttpAsyncClients.createDefault();
        httpclient.start();
        HttpPost httpPost = new HttpPost("http://localhost:12581/update");
        List<NameValuePair> nvps = new ArrayList<>();
        nvps.add(new BasicNameValuePair("url", "http://localhost:8080/status/handler"));
        nvps.add(new BasicNameValuePair("id", trainUpdate.getTrainupdateid().toString()));
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
            }
            @Override
            public void cancelled() {
                System.out.println(httpPost.getRequestLine() + " cancelled");
                System.out.println(" callback thread id is : " + Thread.currentThread().getId());
            }
        });

        return ResponseUtil.wrapResponse(1, "updatesuccess", trainUpdate.getTrainupdateid());
    }

    @ResponseBody
    @RequestMapping(value = "prepareData")
    public JSONObject prepareData(@RequestParam(value = "equalHist") Boolean equalHist) {
        String srcDir = path.getUserFacePath();
        String outDir = path.getTrainPath();
        File src = new File(srcDir);
        File out = new File(outDir);
        if (!src.exists()) {
            return ResponseUtil.wrapResponse(2, "源文件夹不存在", "");
        }
        LinkedList<File> files = new LinkedList<>();
        files.add(src);
        File f;
        while (!files.isEmpty()) {
            f = files.pop();
            System.out.println(f.getName());
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
