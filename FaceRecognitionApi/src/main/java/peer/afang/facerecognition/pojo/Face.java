package peer.afang.facerecognition.pojo;

import java.util.Date;

public class Face {
    private Integer faceid;

    private Integer userid;

    private String imagename;

    private Date time;

    private String srcpath;

    private String facepath;

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
        this.imagename = imagename == null ? null : imagename.trim();
    }

    public Date getTime() {
        return time;
    }

    public void setTime(Date time) {
        this.time = time;
    }

    public String getSrcpath() {
        return srcpath;
    }

    public void setSrcpath(String srcpath) {
        this.srcpath = srcpath;
    }

    public String getFacepath() {
        return facepath;
    }

    public void setFacepath(String facepath) {
        this.facepath = facepath;
    }

    @Override
    public String toString() {
        return "Face{" +
                "faceid=" + faceid +
                ", userid=" + userid +
                ", imagename='" + imagename + '\'' +
                ", time=" + time +
                ", srcpath='" + srcpath + '\'' +
                ", facepath='" + facepath + '\'' +
                '}';
    }
}