<template>
  <div>
    <div id="adduser-div">
      <el-button size="small" type="primary" icon="el-icon-plus" @click="outdialogVisible = true">新建用户</el-button>
      <el-dialog title="新建用户" :visible.sync="outdialogVisible" width="30%" @close="handleClose">
        <el-input ref="adduserinput" v-model="username" placeholder="请输入用户名"></el-input>
        <p id="message">{{ message }}</p>
        <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="outdialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="addUser">确 定</el-button>
        </span>
      </el-dialog>
    </div>
    <div id="userlist-div">
      <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column prop="userid" label="id" width="180">
        </el-table-column>
        <el-table-column prop="username" label="姓名" width="180">
        </el-table-column>
        <el-table-column prop="time" label="创建时间">
        </el-table-column>
        <el-table-column prop="faces" label="照片数量">
        </el-table-column>
        <el-table-column prop="faces" label="">
          <template slot-scope="scope">
            <router-link :to="{ name: 'Userinfo', query: { userid: scope.row.userid, username: scope.row.username }}">详细信息</router-link>
          </template>
        </el-table-column>
        <el-table-column prop="faces" label="">
          <template slot-scope="scope">
            <el-button type="text" @click="editUser(scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination @current-change="handleCurrentChange" layout="prev, pager, next" :page-size=10 :total="countuser">
      </el-pagination>
      <el-dialog title="编辑用户" :visible.sync="updatedialogVisible" width="30%" @close="handleClose">
        <el-input ref="adduserinput" v-model="u.username" placeholder="请输入用户名"></el-input>
        <p id="message">{{ message }}</p>
        <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="updatedialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="updateUser()">确 定</el-button>
        </span>
      </el-dialog>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'Userboard',
  data () {
    return {
      u:{},
      updatedialogVisible: false,
      message: '',
      username: '',
      outdialogVisible: false,
      countuser: 2000,
      tableData: [{
        userid: 1,
        username: '张振方',
        time: 'asdf',
        faces: '12'
      },
      {
        userid: 2,
        username: '张振方',
        time: 'asdf',
        faces: '12'
      },
      {
        userid: 3,
        username: '张振方',
        time: 'asdf',
        faces: '12'
      }]
    }
  },
  methods: {
    editUser (user) {
      this.u = user
      this.updatedialogVisible = true
    },
    handleClose () {
      this.message = '',
      this.username = ''
    },
    updateUser () {
      this.axios.post('http://localhost:8080/user/updateUser', this.qs.stringify(this.u)).then((response) => {
        if (response.data.status === 1) {
          this.updatedialogVisible = false
          this.$message(response.data.message)
        } else if (response.data.status === 2) {
          this.message = response.data.message
        }
      })
    },
    addUser () {
      if (this.username === '') {
        this.$message('请输入用户名')
        this.$refs['adduserinput'].focus()
        return
      }
      this.axios.post('http://localhost:8080/user/addUser', this.qs.stringify({
        userName: this.username
      })).then((response) => {
        if (response.data.status === 1) {
          this.outdialogVisible = false
          this.tableData.push(response.data.data)
          this.$message(response.data.message)
        } else if (response.data.status === 2) {
          this.message = response.data.message
        }
      })
    },
    handleClick (row) {
      console.log(row.name)
    },
    handleCurrentChange (val) {
      var u = this.tableData[this.tableData.length - 1]
      console.log(u.date, val)
    },
    listNextPage (startid, pageSize) {
      this.axios.post('http://localhost:8080/user/listAllUser', this.qs.stringify({
        startid: startid,
        pageSize: pageSize
      })).then((response) => {
        console.log(response)
        if (response.data.status === 1) {
          this.tableData = response.data.data
        } else {
          this.$message('查询失败')
        }
      })
    },
    countAllUser () {
      this.axios.get('http://localhost:8080/user/countAllUser').then((response) => {
        console.log(response)
        if (response.data.status === 1) {
          this.countuser = response.data.data
        } else {
          this.$message('查询失败')
        }
      })
    }
  },
  mounted () {
    this.$emit('changeBread', 'userboard')
    this.countAllUser()
    this.listNextPage(0, 10)
  }
}
</script>

<style>
#adduser-div {
  margin-top: 10px;
  text-align: left;
}
#userlist-div {
  margin-top: 10px;
}
#message {
  color: red;
}
</style>
