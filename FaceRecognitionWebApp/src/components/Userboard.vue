<template>
  <div>
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
        <!-- <el-button @click="handleClick(scope.row)" type="text" size="small">详细信息</el-button> -->
      </template>
    </el-table-column>
  </el-table>
  <el-pagination @current-change="handleCurrentChange" layout="prev, pager, next" :page-size=10 :total="countuser">
  </el-pagination>
  </div>
</template>

<script>
export default {
  name: 'Userboard',
  data () {
    return {
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

</style>
