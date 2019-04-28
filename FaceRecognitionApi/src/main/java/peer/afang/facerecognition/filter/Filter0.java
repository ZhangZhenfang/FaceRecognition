package peer.afang.facerecognition.filter;

import com.alibaba.fastjson.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.RequestMethod;
import peer.afang.facerecognition.enums.OriginControlTypeEnum;
import peer.afang.facerecognition.property.OriginControl;
import peer.afang.facerecognition.property.Path;

import javax.annotation.Resource;
import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * @author ZhangZhenfang
 * @date 2019/4/1 10:49
 */
@Component
@WebFilter(dispatcherTypes = DispatcherType.REQUEST)
public class Filter0 implements Filter {
    private static final Logger LOGGER = LoggerFactory.getLogger(Filter0.class);
    @Resource
    private Path path;
    @Resource
    private OriginControl originControl;

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        LOGGER.debug("Filter0 inited");

        System.load(path.getOpencvPath());
        LOGGER.info("{} loaded", path.getOpencvPath());
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain)
            throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) servletRequest;
        HttpServletResponse response = (HttpServletResponse) servletResponse;
        Object user = request.getSession().getAttribute("user");
        int originControlType = originControl.getOriginControlType();
        String origin = request.getHeader("Origin");
        String method = request.getMethod();
        String url = request.getRequestURL().toString();
        String uri = request.getRequestURI();
        LOGGER.info("{}, {}, {}", origin, method, uri);
        if (uri.contains("face/") || uri.contains("model/fakeReal") || origin.equals("https://www.the15373.com")
                || origin.equals("http://localhost:8081") || uri.contains("model/verify") || url.contains("css")
                || url.contains("js") || url.contains("font") || url.contains("index") || url.contains("localhost")) {
            response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_ORIGIN, origin);
            response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_CREDENTIALS, String.valueOf(true));
            response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_METHODS, method);
            response.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
            filterChain.doFilter(servletRequest, servletResponse);
        } else {
            if (user == null && !request.getRequestURI().endsWith("login")) {
                response.setHeader("Content-Type", "application/json");
                JSONObject jo = new JSONObject();
                jo.put("status", 0);
                response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_ORIGIN, origin);
                response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_CREDENTIALS, String.valueOf(true));
                response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_METHODS, method);
                response.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
                response.getWriter().write(jo.toString());
                return;
            }
            if (originControlType == OriginControlTypeEnum.ALLOW_ALL.getType()) {
                response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_ORIGIN, origin);
                response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_CREDENTIALS, String.valueOf(true));
                response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_METHODS, method);
                response.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
                filterChain.doFilter(servletRequest, servletResponse);
            } else if (originControlType == OriginControlTypeEnum.BLACK.getType()) {
                if (!originControl.getOrigins().contains(origin)) {
                    response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_ORIGIN, origin);
                    response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_CREDENTIALS, String.valueOf(true));
                    response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_METHODS, method);
                    response.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
                    filterChain.doFilter(servletRequest, servletResponse);
                }
            } else {
                if (originControl.getOrigins().contains(origin)) {
                    response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_ORIGIN, origin);
                    response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_CREDENTIALS, String.valueOf(true));
                    response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_METHODS, method);
                    response.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
                    filterChain.doFilter(servletRequest, servletResponse);
                }
            }
        }
    }

    @Override
    public void destroy() {
        LOGGER.debug("Filter0 destroyed");
    }
}
