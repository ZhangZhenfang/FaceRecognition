<template>
  <div>
    <div class="bread-div">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item v-for="bread in breads[breadIndex]" v-bind:key="bread.path" :to="bread.path">{{ bread.title }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div id="addface-div">
      <div id="currentuser-div">
        当前用户：{{ username }}, 共{{ faces.length }}张
      </div>
      <div id="newface-div">
        <el-button type="primary" size="small" icon="el-icon-plus" @click="outdialogVisible = true">添加人脸图像</el-button>
        <el-button type="primary" size="small" icon="el-icon-plus" @click="videodialogVisible = true">视频添加人脸</el-button>
        <el-dialog title="添加人脸" :visible.sync="outdialogVisible" width="30%" :before-close="handleClose">
          <el-upload action="https://jsonplaceholder.typicode.com/posts/" list-type="picture-card" multiple
            :on-preview="handlePictureCardPreview" :on-remove="handleRemove" :auto-upload="false" ref="upload" :http-request="uploadfile">
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-dialog :visible.sync="dialogVisible" size="tiny">
            <img width="100%" :src="dialogImageUrl" alt="">
          </el-dialog>
          <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="upload()">上 传</el-button>
            <el-button type="primary" @click="handleClose">确 定</el-button>
          </span>
        </el-dialog>

        <el-dialog title="添加人脸" :visible.sync="videodialogVisible" width="30%" :before-close="handleClose">
          <Video></Video>
        </el-dialog>
      </div>
    </div>
    <div id="userface-div" v-for="face in this.faces" v-bind:key="face.id">
      <el-card :body-style='{ padding: "10px", height: "360px"}' width="100px">
        <div id="facdimg-div">
          <img :src="'http://localhost:8080/' + face.url" class="image">
        </div>
        <div style="padding: 14px;">
          <div class="bottom clearfix">
            <time class="time">上传时间：{{ face.time }}</time>
            <el-button type="text" class="button" @click="deleteFace(face.faceid)">删除</el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import Video from './Video'

export default {
  name: 'Userinfo',
  components: { Video },
  data () {
    return {
      videodialogVisible: false,
      breads: {},
      breadIndex: '',
      userid: 0,
      username: '',
      outdialogVisible: false,
      dialogVisible: false,
      dialogImageUrl: '',
      faces: []
    }
  },
  methods: {
    deleteFace (faceid) {
      this.axios.delete('http://localhost:8080/face/face/' + faceid).then((response) => {
        if (response.status === 200) {
          if (response.data.status === 1) {
            for (var i = 0; i < this.faces.length; i++) {
              if (this.faces[i].faceid === faceid) {
                this.faces.splice(i, 1)
              }
            }
            this.$message('删除成功')
          } else {
            this.$message('删除人脸失败')
          }
        }
      })
    },
    getFacesByUserid (userid) {
      // console.log(userid)
      this.axios.get('http://localhost:8080/face/listByUserid?userid=' + userid).then((response) => {
        if (response.status === 200) {
          if (response.data.status === 1) {
            this.faces = response.data.data
          } else {
            this.$message('获取人脸失败')
          }
        }
      })
    },
    upload () {
      this.$refs['upload'].submit()
    },
    uploadfile (file, fileList) {
      var filedata = new FormData()
      filedata.append('data', file.file)
      filedata.append('userName', this.username)
      var config = {
        onUploadProgress: file.onProgress
      }
      this.axios.post('http://localhost:8080/face/addFace', filedata, config).then((response) => {
        // console.log(response.data.status)
        if (response.data.status === 1) {
          this.faces.push(response.data.data)
          file.onSuccess(response)
        } else if (response.data.status === 3) {
          this.message(file.file.name + '未检测到人脸')
          file.onError(response)
        } else if (response.data.status === 4) {
          this.message(file.file.name + '检测到多张人脸')
          file.onError(response)
        }
      })
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          this.$refs['upload'].clearFiles()
          this.outdialogVisible = false
          done()
        })
        .catch(_ => {})
    },
    handleRemove (file, fileList) {
      // console.log(file, fileList)
    },
    handlePictureCardPreview (file) {
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    }
  },
  mounted () {
    this.breads = this.$route.params.breads
    this.breadIndex = 'userinfo'
    this.userid = this.$route.query.userid
    this.username = this.$route.query.username
    this.getFacesByUserid(this.userid)
  }
}
</script>

<style>
#addface-div {
  width:600px;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-left: 0px;
  text-align: left;
}
#currentuser-div {
  margin-top: 5px;
}
#newface-div {
  margin-top: 5px;
  width: 100%;
}
#userface-div {
  width: 290px;
  height: 380px;
  float: left;
  margin-right: 10px;
  border: whitesmoke solid 1px;
}
#facdimg-div{
  width: 100%;
  height: 300px;
}
.time {
  font-size: 13px;
  color: #999;
}
.bottom {
  margin-top: 13px;
  line-height: 12px;
}
.button {
  padding: 0;
  float: right;
}
.image {
  max-width: 100%;
  max-height: 300px;
}
.clearfix:before,
.clearfix:after {
    display: table;
    content: "";
}
.clearfix:after {
    clear: both
}
</style>
