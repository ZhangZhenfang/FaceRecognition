package peer.afang.facerecognition.vo;

import java.util.Date;

/**
 * @author ZhangZhenfang
 * @date 2019/4/9 21:13
 */
public class UserInfoVO {
    private Integer userid;

    private String username;

    private Date time;

    private Integer faces;

    public Integer getUserid() {
        return userid;
    }

    public void setUserid(Integer userid) {
        this.userid = userid;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public Date getTime() {
        return time;
    }

    public void setTime(Date time) {
        this.time = time;
    }

    public Integer getFaces() {
        return faces;
    }

    public void setFaces(Integer faces) {
        this.faces = faces;
    }

    @Override
    public String toString() {
        return "UserInfoVO{" +
                "userid=" + userid +
                ", username='" + username + '\'' +
                ", time=" + time +
                ", faces=" + faces +
                '}';
    }
}
