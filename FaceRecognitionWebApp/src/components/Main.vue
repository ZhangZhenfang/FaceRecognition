<template>
  <div>
    <el-container>
    <el-header>
      this is header
    </el-header>
    <el-container>
      <el-aside width="200px">
        <Menu></Menu>
      </el-aside>
      <el-main>
        <Userboard></Userboard>
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
      message: 'main'
    }
  }
}
</script>

<style>
.el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
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
