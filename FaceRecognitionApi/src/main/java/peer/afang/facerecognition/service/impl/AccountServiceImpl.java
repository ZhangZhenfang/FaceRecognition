package peer.afang.facerecognition.service.impl;

import org.springframework.stereotype.Service;
import peer.afang.facerecognition.mapper.AccountMapper;
import peer.afang.facerecognition.pojo.Account;
import peer.afang.facerecognition.service.AccountService;

import javax.annotation.Resource;

/**
 * @author ZhangZhenfang
 * @date 2019/4/27 19:34
 */
@Service
public class AccountServiceImpl implements AccountService {
    @Resource
    AccountMapper accountMapper;

    @Override
    public Account getByAccount(String account) {
        return accountMapper.getByAccount(account);
    }
}
