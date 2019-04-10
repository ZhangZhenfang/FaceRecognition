<template>
  <div>
    <el-container>
    <el-header>
      this is header
    </el-header>
    <el-container>
      <el-aside width="150px">
        <Menu></Menu>
      </el-aside>
      <el-main>
        <el-breadcrumb separator-class="el-icon-arrow-right">
          <el-breadcrumb-item v-for="bread in breads[breadIndex]" v-bind:key="bread.path" :to="bread.path">{{ bread.title }}</el-breadcrumb-item>
        </el-breadcrumb>
        <router-view @changeBread="changeBread"/>
      </el-main>
    </el-container>
    </el-container>
  </div>
</template>

<script>
import Menu from './Menu'
import Userboard from './Userboard'
export default {
  components: { Menu, Userboard },
  name: 'Main',
  data () {
    return {
      breadIndex: 'index',
      breads: {
        index: [
          {
            path: '/',
            title: '首页'
          }
        ],
        userboard: [
          {
            path: '/',
            title: '首页'
          },
          {
            path: 'Userboard',
            title: '用户管理'
          }
        ],
        userinfo: [
          {
            path: '/',
            title: '首页'
          },
          {
            path: 'Userboard',
            title: '用户管理'
          },
          {
            path: 'Userinfo',
            title: '用户详情'
          }
        ]
      },
      message: 'main'
    }
  },
  methods: {
    changeBread (index) {
      this.breadIndex = index
    }
  },
  mounted () {
  }
}
</script>

<style>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  height: 20px;
  /* line-height: 60px; */
}
.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
  max-height: 60%;
}
.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  max-height: 60%;
}
body > .el-container {
  margin-bottom: 40px;
}
</style>
