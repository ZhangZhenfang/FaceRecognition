package peer.afang.facerecognition.pojo;

import java.util.Date;

/**
 * @author ZhangZhenfang
 * @date 2019/4/27 19:31
 */
public class Account {

    private String account;
    private Date time;
    private String password;

    public String getAccount() {
        return account;
    }

    public void setAccount(String account) {
        this.account = account;
    }

    public Date getTime() {
        return time;
    }

    public void setTime(Date time) {
        this.time = time;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    @Override
    public String toString() {
        return "Account{" +
                "account='" + account + '\'' +
                ", time=" + time +
                ", password='" + password + '\'' +
                '}';
    }
}
