<template>
  <div id="modelcontrol-div">
      <el-button @click="train" :disabled="disableBtn">训练模型</el-button>
      <el-button @click="update" :disabled="disableBtn">更新模型</el-button>
      <el-button @click="deploy" :disabled="disableBtn">部署模型</el-button>
      <div id="steps-div"><span v-html="steps"></span></div>
  </div>
</template>

<script>
import { setInterval, setTimeout } from 'timers';
export default {
  name: 'ModelControl',
  data () {
    return {
      disableBtn: false,
      steps: '',
      interval: {},
      trainupdateid: 0
    }
  },
  methods: {
    train () {
    },
    deploy () {
      this.axios.get('http://localhost:8080/model/restore').then(response => {
        console.log(response)
        if (response.data.status === 1) {
          this.$message('部署成功')
        } else {
          this.$message('部署失败')
        }
      })
    },
    update () {
      this.disableBtn = true
      this.axios.get('http://localhost:8080/trainupdate/update').then(response => {
        console.log(response)
        if (response.data.status === 1) {
          this.trainupdateid = response.data.data
        }
        this.interval = setTimeout(this.getSteps, 1000)
      })
    },
    getSteps () {
      var that = this
      this.axios.post('http://localhost:8080/status/getSteps', this.qs.stringify({
        trainupdateid: this.trainupdateid
      })).then(response => {
        if (response.data.status === 1) {
          if (response.data.message === 'stop') {
            this.disableBtn = false
            this.$message('success')
          } else {
            this.steps = []
            var stepstr = ''
            var steps = response.data.data
            for (var i = 0; i < steps.length; i++) {
              stepstr += steps[i] + '<br>'
            }
            this.steps = stepstr
            setTimeout(this.getSteps, 1000)
          }
        }
      })
    }
  }
}
</script>

<style>
#steps-div {
  font-size: 23px;
}
</style>
