<template>
  <div id="menu-div">
    <div id="account">
      {{ account }} <el-button type="text" @click="logout">注销</el-button>
    </div>
    <el-menu :default-active="menuIndex" class="el-menu-vertical-demo" @select="handleSelect" background-color="#545c64"
      text-color="#fff" active-text-color="#ffd04b">
      <el-menu-item index="1">
        <span slot="title">人脸库管理</span>
      </el-menu-item>
      <el-menu-item index="2">
        <span slot="title">模型管理</span>
      </el-menu-item>
      <el-menu-item index="3">
        <span slot="title">实时识别</span>
      </el-menu-item>
      <el-menu-item index="4">
        <span slot="title">图片识别</span>
      </el-menu-item>
      <!-- <el-menu-item index="5">
        <span slot="title">活体检测</span>
      </el-menu-item> -->
    </el-menu>
  </div>
</template>

<script>
import urls from '../json/URLS'
export default {
  name: 'Menu',
  props: ['menuIndex'],
  data () {
    return {
      account: 'account'
    }
  },
  methods: {
    logout () {
      // console.log('logout')
      this.axios.post(urls.api + '/login/logout').then(response => {
        // this.account = response.data.data
        console.log(response.data.status)
        if (response.data.status === 0 || response.data.status === 1) {
          this.$router.push('/login')
        }
      })
    },
    getAccountInfo () {
      this.axios.post(urls.api + '/login/getAccountInfo').then(response => {
        this.account = response.data.data
      })
    },
    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    },
    handleSelect (key, keyPath) {
      switch (key) {
        case '1':
          this.$router.push('/userboard')
          break
        case '2':
          this.$router.push('/modelcontrol')
          break
        case '3':
          this.$router.push('/recognition')
          break
        case '4':
          this.$router.push('/imageRecognition')
          break
        // case '5':
        //   this.$router.push('/live')
        //   break
        default:
          this.$router.push('/')
      }
    }
  },
  mounted () {
    this.handleSelect('1')
    this.getAccountInfo()
  }
}
</script>

<style>

</style>
