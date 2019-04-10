package peer.afang.facerecognition.filter;

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
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain)
            throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) servletRequest;
        HttpServletResponse response = (HttpServletResponse) servletResponse;

        int originControlType = originControl.getOriginControlType();
        String origin = request.getHeader("Origin");

        if (originControlType == OriginControlTypeEnum.ALLOW_ALL.getType()) {
            response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_ORIGIN, origin);
            response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_METHODS, RequestMethod.DELETE.name());
            filterChain.doFilter(servletRequest, servletResponse);
        } else if (originControlType == OriginControlTypeEnum.BLACK.getType()) {
            if (!originControl.getOrigins().contains(origin)) {
                response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_ORIGIN, origin);
                filterChain.doFilter(servletRequest, servletResponse);
            }
        } else {
            if (originControl.getOrigins().contains(origin)) {
                response.setHeader(HttpHeaders.ACCESS_CONTROL_ALLOW_ORIGIN, origin);
                filterChain.doFilter(servletRequest, servletResponse);
            }
        }
    }

    @Override
    public void destroy() {
        LOGGER.debug("Filter0 destroyed");
    }
}
