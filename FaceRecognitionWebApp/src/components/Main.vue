<template>
  <div>
    <el-container>
    <el-header>
      this is header
    </el-header>
    <el-container>
      <el-aside width="150px">
        <Menu :menuIndex="menuIndex" ></Menu>
      </el-aside>
      <el-main>
        <router-view @changeMenuIndex="changeMenuIndex"/>
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
      menuIndex: '1',
      message: 'main'
    }
  },
  methods: {
    changeMenuIndex (index) {
      this.menuIndex = index
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
}
.el-aside {
  background-color: #545c64;
  color: #333;
  text-align: center;
  max-height: 60%;
}
.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  min-height: 900px;
}
.el-breadcrumb {
  font-size: 17px;
}
body > .el-container {
  margin-bottom: 40px;
}
</style>
