<template>
  <div id="live-div">
    <div id="livecanvas-div">
      <video v-show="showVideo" id="livevideo"></video>
      <canvas v-show="showCanvas" id="livecanvas"></canvas>
      <img v-show="showImg" id="liveimg" width="640" height="480"/>
    </div>
    <div id="livevideo-op-div">
      <el-button @click="handleOpenVideo">开启摄像头</el-button>
      <el-button @click="handleCloseVideo">关闭摄像头</el-button>
    </div>
  </div>
</template>

<script>
import urls from '../json/URLS'
export default {
  name: 'Live',
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
      } else {
        this.stop = true
      }
      this.stream = null
      this.stop = true
    },
    snapAndUpload () {
      var file = this.takecapture()
      this.currentPic = file
      var formData = new FormData()
      console.log(file)
      formData.append('data', file)
      this.axios.post(urls.api + '/model/fakeRealPlus', formData).then(response => {
        this.img.src = 'data:image/jpg;base64,' + response.data
        if (!this.stop) {
          setTimeout(this.snapAndUpload, 300)
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
    this.canvas = document.getElementById('livecanvas')
    this.video = document.getElementById('livevideo')
    this.img = document.getElementById('liveimg')
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
