package peer.afang.facerecognition.pojo;

public class Face {
    private Integer faceid;

    private Integer userid;

    private String imagename;

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

    @Override
    public String toString() {
        return "Face{" +
                "faceid=" + faceid +
                ", userid=" + userid +
                ", imagename='" + imagename + '\'' +
                '}';
    }
}