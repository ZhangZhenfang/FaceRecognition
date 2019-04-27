package peer.afang.facerecognition.mapper;

import peer.afang.facerecognition.pojo.Account;

/**
 * @author ZhangZhenfang
 * @date 2019/4/27 19:33
 */
public interface AccountMapper {

    Account getByAccount(String account);
}
