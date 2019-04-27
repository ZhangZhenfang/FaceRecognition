package peer.afang.facerecognition.service;

import peer.afang.facerecognition.pojo.Account;

/**
 * @author ZhangZhenfang
 * @date 2019/4/27 19:34
 */
public interface AccountService {

    Account getByAccount(String account);
}
