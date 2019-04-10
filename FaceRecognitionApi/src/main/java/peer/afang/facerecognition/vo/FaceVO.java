package peer.afang.facerecognition.vo;

import java.util.Date;

/**
 * @author ZhangZhenfang
 * @date 2019/4/10 16:39
 */
public class FaceVO {
    private Integer faceid;

    private Integer userid;

    private String imagename;

    private Date time;

    private String url;

    public Integer getFaceid() {
        return faceid;
    }

    public void setFaceid(Integer faceid) {
        this.faceid = faceid;
    }

    public Integer getUserid() {
        return userid;
    }

    public void setUserid(Integer userid) {
        this.userid = userid;
    }

    public String getImagename() {
        return imagename;
    }

    public void setImagename(String imagename) {
        this.imagename = imagename;
    }

    public Date getTime() {
        return time;
    }

    public void setTime(Date time) {
        this.time = time;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    @Override
    public String toString() {
        return "FaceVO{" +
                "faceid=" + faceid +
                ", userid=" + userid +
                ", imagename='" + imagename + '\'' +
                ", time=" + time +
                ", url='" + url + '\'' +
                '}';
    }
}
