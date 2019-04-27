<template>
  <div id="login-div">
    <div id="login-form-div">
      <el-form :model="logingForm" status-icon ref="logingForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="账号" prop="account">
          <el-input type="text" v-model="logingForm.account" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="logingForm.password" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('loginForm')">登录</el-button>
          <el-button @click="resetForm('ruleForm2')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import urls from '../json/urls'
export default {
  name: 'Login',
  data () {
    return {
      logingForm: {
        account: '',
        password: ''
      }
    }
  },
  methods: {
    submitForm (formName) {
      if (this.logingForm.account === '') {
        this.$message('请输入账号')
        return
      }
      if (this.logingForm.password === '') {
        this.$message('请输入密码')
        return
      }
      this.axios.post(urls.api + '/login/login', this.qs.stringify({
        account: this.logingForm.account,
        password: this.logingForm.password
      })).then(response => {
        console.log(response)
        if (response.data.status === 1) {
          this.$router.push('/userboard')
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>

<style>
#login-div {
  width: 50%;
  text-align: center;
  margin: 200px auto;
  /* border: 1px solid black; */
}
#login-form-div {
  width: 600px;
  /* border: 1px solid red; */
}
</style>
