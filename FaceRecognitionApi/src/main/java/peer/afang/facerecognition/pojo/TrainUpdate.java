package peer.afang.facerecognition.pojo;

import java.util.Date;

/**
 * @author ZhangZhenfang
 * @date 2019/4/13 14:44
 */
public class TrainUpdate {
    private Integer trainupdateid;
    private Date time;
    private String status;
    private String param;
    private String log;
    private String version;

    public Date getTime() {
        return time;
    }

    public void setTime(Date time) {
        this.time = time;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getParam() {
        return param;
    }

    public void setParam(String param) {
        this.param = param;
    }

    public Integer getTrainupdateid() {
        return trainupdateid;
    }

    public void setTrainupdateid(Integer trainupdateid) {
        this.trainupdateid = trainupdateid;
    }

    public String getLog() {
        return log;
    }

    public void setLog(String log) {
        this.log = log;
    }

    public String getVersion() {
        return version;
    }

    public void setVersion(String version) {
        this.version = version;
    }

    @Override
    public String toString() {
        return "TrainUpdate{" +
                "trainupdateid=" + trainupdateid +
                ", time=" + time +
                ", status='" + status + '\'' +
                ", param='" + param + '\'' +
                ", log='" + log + '\'' +
                ", version='" + version + '\'' +
                '}';
    }
}
