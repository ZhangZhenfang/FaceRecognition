<template>
  <div id="addfacevideo-div">
    <video id="video"></video>
    <button id="btn" onclick="start()">start</button>
    <button id="stopbtn" onclick="stop()">stop</button>
    <canvas id="canvas"></canvas>
    <img id="img" width="320" height="240"/>
  </div>
</template>

<script>
export default {
  name: 'Video',
  data () {
    return {
      convas: {},
      video: {},
      img: {},
      btn: {},
      context: {},
      width: 320,
      height: 240,
      streaming: false,
      interveal:{}
    }
  },
  methods: {
    start () {
      this.interveal = setInterval(this.snapAndUpload, 200)
    },
    stop () {
        clearInterval(this.interveal)
    },

    snapAndUpload () {
      var file = this.takecapture()
      var formData = new FormData()
      formData.append('data', file)
      // this.axios('http://localhost:8080/model/detect', ).then(response => {
      //   img.src = "data:image/png;base64," + response
      // })
    },
    takecapture () {
      if (this.streaming) {
          this.context.drawImage(this.video, 0, 0, 320, 240)
          return this.DataURL2Blob(this.canvas.toDataURL('img/png'), 'png')
      }
    },

    DataURL2Blob (dataURL, type){
      var bytes = window.atob(dataURL.split(",")[1])
      var ab = new ArrayBuffer(bytes.length)
      var ia = new Uint8Array(ab)
      for (var i = 0; i < bytes.length; i++) {
          ia[i] = bytes.charCodeAt(i)
      }
      return new Blob([ab], { type : 'image/' + type })
    }
  },
  mounted () {
    this.convas = document.getElementById('canvas')
    this.video = document.getElementById('video')
    this.img = document.getElementById('img')
    this.btn = document.getElementById('btn')
    this.context = canvas.getContext('2d')
    navigator.mediaDevices.getUserMedia({video: true, audio: false}).then(stream => {
      this.video.srcObject = stream
      this.video.play()
      this.interveal = setInterval(this.snapAndUpload, 1000)
    })
    // var that = this
    // 监听视频流就位事件,即视频可以播放了
    this.video.addEventListener('canplay', (ev) => {
      if (!this.streaming) {
        this.video.setAttribute('width', this.width)
        this.video.setAttribute('height', this.height)
        // this.canvas.setAttribute('width', this.width)
        // this.canvas.setAttribute('height', this.height)
        this.streaming = true
      }
    }, false)
  }
}
</script>

<style>

</style>
