<template>
  <div id="addfacevideo-div">
    <!-- <button id="btn" @click="start()">start</button>
    <button id="stopbtn" @click="stop()">stop</button> -->
    <div id="canvas-div">
      <video v-show="showVideo" id="video"></video>
      <canvas v-show="showCanvas" id="canvas"></canvas>
      <img v-show="showImg" id="img" width="320" height="240"/>
    </div>
    <div id="video-op-div">
      <el-button @click="snapAndUpload">拍照</el-button>
      <el-button @click="addFace" v-bind:disabled="addable">添加</el-button>
      <el-button @click="reset" v-bind:disabled="resetable">重新拍照</el-button>
    </div>
  </div>
</template>

<script>
export default {
  props: ['stream', 'username', 'faces'],
  name: 'Video',
  data () {
    return {
      currentPic: {},
      showVideo: true,
      showCanvas: false,
      showImg: false,
      addable: true,
      resetable: true,
      canvas: {},
      video: {},
      img: {},
      btn: {},
      context: {},
      width: 320,
      height: 240,
      streaming: false,
      interveal: {}
    }
  },
  methods: {
    addFace () {
      this.addable = true
      var filedata = new FormData()
      filedata.append('data', this.currentPic)
      filedata.append('userName', this.username)
      this.axios.post('http://localhost:8080/face/addFace', filedata).then((response) => {
        if (response.data.status === 1) {
          this.faces.push(response.data.data)
          this.$message(response.data.message)
        } else if (response.data.status === 3) {
          this.$message('未检测到人脸')
        } else if (response.data.status === 4) {
          this.$message('检测到多张人脸')
        }
      })
    },
    reset () {
      this.addable = true
      this.resetable = true
      this.showVideo = true
      this.showImg = false
    },
    snapAndUpload () {
      var file = this.takecapture()
      this.currentPic = file
      var formData = new FormData()
      formData.append('data', file)
      this.axios.post('http://localhost:8080/model/detect', formData).then(response => {
        this.img.src = 'data:image/png;base64,' + response.data
      })
    },
    takecapture () {
      this.addable = false
      this.resetable = false
      this.showVideo = false
      this.showImg = true
      if (this.streaming) {
        this.context.drawImage(this.video, 0, 0, 320, 240)
        return this.DataURL2Blob(this.canvas.toDataURL('img/png'), 'png')
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
  watch: {
    'stream': function (val) {
      if (val === null) {
        clearInterval(this.interveal)
      } else {
        this.video.srcObject = this.stream
        this.video.play()
        // this.interveal = setInterval(this.snapAndUpload, 300)
      }
    }
  },
  mounted () {
    this.canvas = document.getElementById('canvas')
    this.video = document.getElementById('video')
    this.img = document.getElementById('img')
    this.btn = document.getElementById('btn')
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
#addfacevideo-div{
  text-align: center;
  width: 100%;
}
#canvas-div {
  text-align: center;
  width: 100%;
}
#canvas-div img{
  /* text-align: center; */
  padding-left: 0px;
  width: 320px;
}

</style>
