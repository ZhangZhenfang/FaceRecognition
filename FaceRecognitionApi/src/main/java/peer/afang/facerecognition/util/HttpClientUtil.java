package peer.afang.facerecognition.util;

import org.apache.http.HttpEntity;
import org.apache.http.NameValuePair;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.util.StringUtils;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Set;

/**
 * @author ZhangZhenfang
 * @date 2019/4/7 12:17
 */
public class HttpClientUtil {
    private static final Logger LOGGER = LoggerFactory.getLogger(HttpClientUtil.class);

    public static String PostFiles(String uri, List<String> filePaths, HashMap<String, String> parms) {
        if (filePaths.size() == 0) {
            return null;
        }
        CloseableHttpClient client = HttpClientBuilder.create().build();
        CloseableHttpResponse response = null;
        HttpPost post = new HttpPost(uri);
        RequestConfig requestConfig = RequestConfig.custom().setConnectTimeout(1000).setSocketTimeout(1200).build();
        post.setConfig(requestConfig);
        MultipartEntityBuilder multipartEntityBuilder = MultipartEntityBuilder.create();
        for (String s : filePaths) {
            multipartEntityBuilder.addBinaryBody("data", new File(s));
        }
        Set<String> strings = parms.keySet();
        for (String key : strings) {
            multipartEntityBuilder.addTextBody(key, parms.get(key));
        }
        HttpEntity httpEntity = multipartEntityBuilder.build();
        post.setEntity(httpEntity);
        StringBuilder sb = new StringBuilder();
        try {
            response = client.execute(post);
            int statusCode = response.getStatusLine().getStatusCode();
            if (statusCode == 200) {
                BufferedReader bufferedReader = new BufferedReader(
                        new InputStreamReader(response.getEntity().getContent()));
                String str = "";
                while (!StringUtils.isEmpty(str = bufferedReader.readLine())) {
                    sb.append(str);
                }
                client.close();
                if(response!=null){
                    response.close();
                }

            }

        } catch (IOException e) {
            LOGGER.error("HttpClient IO异常", e);
        }
        return sb.toString();
    }

    public static String post(String uri, HashMap<String, String> parms) {
        CloseableHttpClient client = HttpClientBuilder.create().build();
        CloseableHttpResponse response = null;
        HttpPost post = new HttpPost(uri);
        RequestConfig requestConfig = RequestConfig.custom().setConnectTimeout(1000).setSocketTimeout(1200).build();
        post.setConfig(requestConfig);
        MultipartEntityBuilder multipartEntityBuilder = MultipartEntityBuilder.create();
        Set<String> strings = parms.keySet();
        for (String key : strings) {
            multipartEntityBuilder.addTextBody(key, parms.get(key));
        }
        HttpEntity httpEntity = multipartEntityBuilder.build();
        post.setEntity(httpEntity);
        StringBuilder sb = new StringBuilder();
        try {
            response = client.execute(post);
            int statusCode = response.getStatusLine().getStatusCode();
            if (statusCode == 200) {
                BufferedReader bufferedReader = new BufferedReader(
                        new InputStreamReader(response.getEntity().getContent()));
                String str = "";
                while (!StringUtils.isEmpty(str = bufferedReader.readLine())) {
                    sb.append(str);
                }
                client.close();
                if(response!=null){
                    response.close();
                }

            }

        } catch (IOException e) {
            LOGGER.error("HttpClient IO异常", e);
        }
        return sb.toString();
    }

    public static String get(String uri, HashMap<String, String> parms) {
        CloseableHttpClient httpclient = HttpClients.createDefault();
        List<NameValuePair> params = new ArrayList<NameValuePair>();
        Set<String> set = parms.keySet();
        for (String key : set) {
            params.add(new BasicNameValuePair(key, parms.get(key)));
        }
        //参数转换为字符串
        String paramsStr;
        String url;
        StringBuilder sb = new StringBuilder();
        try {
            paramsStr = EntityUtils.toString(new UrlEncodedFormEntity(params, "UTF-8"));
            url = uri + "?" + paramsStr;
            // 创建httpget.
            HttpGet httpget = new HttpGet(url);
            CloseableHttpResponse response = httpclient.execute(httpget);

            int statusCode = response.getStatusLine().getStatusCode();
            if (statusCode == 200) {
                BufferedReader bufferedReader = new BufferedReader(
                        new InputStreamReader(response.getEntity().getContent()));
                String str = "";
                while (!StringUtils.isEmpty(str = bufferedReader.readLine())) {
                    sb.append(str);
                }
                httpclient.close();
                if(response!=null){
                    response.close();
                }

            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // 关闭连接,释放资源
            try {
                httpclient.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return sb.toString();
    }
}
