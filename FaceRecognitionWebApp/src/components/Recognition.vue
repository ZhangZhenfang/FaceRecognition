<template>
  <div id="recognition-div">
    <div id="recognitioncanvas-div">
      <video v-show="showVideo" id="recognitionvideo"></video>
      <canvas v-show="showCanvas" id="recognitioncanvas"></canvas>
      <img v-show="showImg" alt="选择图片" id="recognitionimg" width="640" height="480"/>
    </div>
    <div id="recognitionvideo-op-div">
      <el-button @click="handleOpenVideo">开启摄像头</el-button>
      <el-button @click="handleCloseVideo">关闭摄像头</el-button>
    </div>
  </div>
</template>

<script>
import urls from '../json/URLS'
export default {
  name: 'Recognition',
  data () {
    return {
      showVideo: false,
      showCanvas: false,
      showImg: true,
      stream: {},
      canvas: {},
      img: {},
      video: {},
      height: 240,
      width: 320,
      stop: false
    }
  },
  methods: {
    handleOpenVideo () {
      navigator.mediaDevices.getUserMedia({ video: true, audio: false }).then(stream => {
        this.stream = stream
        this.video.srcObject = this.stream
        this.video.play()
        this.stop = false
        setTimeout(this.snapAndUpload, 200)
      })
    },
    handleCloseVideo (done) {
      if (this.stream !== undefined && this.stream != null) {
        this.stream.getTracks()[0].stop()
      }
      this.stream = null
      this.stop = true
      this.img.src = ''
    },
    snapAndUpload () {
      var file = this.takecapture()
      this.currentPic = file
      var formData = new FormData()
      console.log(file)
      formData.append('data', file)
      this.axios.post(urls.api + '/model/detectPlus', formData).then(response => {
        if (!this.stop) {
          this.img.src = 'data:image/jpg;base64,' + response.data
          setTimeout(this.snapAndUpload, 100)
        }
      })
    },
    takecapture () {
      this.showVideo = false
      this.showImg = true
      if (this.streaming) {
        this.context.drawImage(this.video, 0, 0, 320, 240)
        return this.DataURL2Blob(this.canvas.toDataURL('img/jpg'), 'jpg')
      }
    },

    DataURL2Blob (dataURL, type) {
      var bytes = window.atob(dataURL.split(',')[1])
      var ab = new ArrayBuffer(bytes.length)
      var ia = new Uint8Array(ab)
      for (var i = 0; i < bytes.length; i++) {
        ia[i] = bytes.charCodeAt(i)
      }
      return new Blob([ab], { type: 'image/' + type })
    }
  },
  mounted () {
    this.canvas = document.getElementById('recognitioncanvas')
    this.video = document.getElementById('recognitionvideo')
    this.img = document.getElementById('recognitionimg')
    this.context = this.canvas.getContext('2d')
    this.video.addEventListener('canplay', (ev) => {
      if (!this.streaming) {
        this.video.setAttribute('width', this.width)
        this.video.setAttribute('height', this.height)
        this.canvas.setAttribute('width', this.width)
        this.canvas.setAttribute('height', this.height)
        this.streaming = true
      }
    }, false)
  }
}
</script>

<style>

</style>
