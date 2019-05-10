<template>
  <div id="image-recognition-div">
    <div id="image-recognition-img-div">
      <el-upload
        action=""
        :show-file-list="false"
        :file-list="fileList"
        :auto-upload="false"
        :http-request="uploadfile"
        ref="upload"
        :on-change="handleChange">
        <el-button :disabled="disableSelect" size="small" type="primary">选择图片</el-button>
      </el-upload>
      <img id="image-recognition-img" src="" alt="" srcset="">
    </div>
  </div>
</template>

<script>
import urls from '../json/urls'
export default {
  name: 'ImageRecognition',
  data () {
    return {
      disableSelect: false,
      img: {},
      fileList: []
    }
  },
  methods: {
    handleChange (file, fileList) {
      this.fileList = []
      this.fileList[0] = file
      var reader = new FileReader()
      reader.onloadend = () => {
        this.img.src = reader.result
        this.disableSelect = true
        this.upload()
      }
      reader.readAsDataURL(file.raw)
    },
    upload () {
      this.$refs['upload'].submit()
    },
    uploadfile (file, fileList) {
      var filedata = new FormData()
      filedata.append('data', file.file)
      var config = {
      }
      this.axios.post(urls.api + '/model/detectPlus', filedata, config).then((response) => {
        this.img.src = 'data:image/jpg;base64,' + response.data
        this.disableSelect = false
      })
    }
  },
  mounted () {
    console.log(document.getElementById('image-recognition-img'))
    this.img = document.getElementById('image-recognition-img')
  }
}
</script>

<style>
#image-recognition-img {
  max-height: 800px;
  max-width: 900px;
}
</style>
