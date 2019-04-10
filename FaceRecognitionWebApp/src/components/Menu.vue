<template>
  <div>
    <el-menu :default-active="menuIndex" class="el-menu-vertical-demo" @select="handleSelect" background-color="#545c64"
      text-color="#fff" active-text-color="#ffd04b">
      <el-menu-item index="1">
        <i class="el-icon-menu"></i>
        <span slot="title">人脸库管理</span>
      </el-menu-item>
      <el-menu-item index="2">
        <i class="el-icon-setting"></i>
        <span slot="title">模型管理</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'Menu',
  props: ['menuIndex'],
  methods: {
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
          this.$router.push('/')
          break
        default:
          this.$router.push('/')
      }
    }
  },
  mounted () {
    this.handleSelect('1')
  }
}
</script>

<style>

</style>
