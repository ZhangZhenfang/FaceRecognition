package peer.afang.facerecognition.enums;

/**
 * @author ZhangZhenfang
 * @date 2019/4/1 20:34
 */
public enum OriginControlTypeEnum {
    /**
     * 允许所有源
     */
    ALLOW_ALL("允许所有", 0),
    /**
     * 黑名单
     */
    BLACK("黑名单", 1),
    /**
     * 白名单
     */
    WHITE("白名单", 2);

    private String desc;
    private int type;
    OriginControlTypeEnum(String desc, int type) {
        this.desc = desc;
        this.type = type;
    }

    public String getDesc() {
        return desc;
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }
}
