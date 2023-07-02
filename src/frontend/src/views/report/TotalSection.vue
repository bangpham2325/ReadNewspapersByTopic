<template>
  <el-row :gutter="16">
    <el-col :sm="4" :xs="8">
      <div class="total">
        <h1>Total User</h1>
        <span>{{ report.total }}</span>
      </div>
    </el-col>
    <el-col :sm="4" :xs="8">
      <div class="total">
        <h1>Post</h1>
        <span>{{ report.total_post }}</span>
      </div>
    </el-col>
    <el-col :sm="4" :xs="8">
      <div class="total">
        <h1>Category</h1>
        <span>{{ report.total_category }}</span>
      </div>
    </el-col>
    <el-col :sm="4" :xs="8">
      <div class="total">
        <h1>Admin</h1>
        <span>{{ report.total_admin }}</span>
      </div>
    </el-col>
    <el-col :sm="4" :xs="8">
      <div class="total">
        <h1>Author</h1>
        <span>{{ report.total_author }}</span>
      </div>
    </el-col>
    <el-col :sm="4" :xs="8">
      <div class="total">
        <h1>Users</h1>
        <span>{{ report.total_user }}</span>
      </div>
    </el-col>
  </el-row>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';

@Options({
  props: {
    report: {
      total: 0,
      total_user: 0,
      total_admin: 0,
      total_author: 0,
      total_post: 0,
      total_category: 0
    } as any
  },
})

export default class TotalSection extends Vue {
}
</script>

<style scoped>
.total {
  background: #FFFFFF;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 20px;
}

h1 {
  font-weight: 600;
  font-size: 14px;
  line-height: 19px;
  color: #797D8C;
}

span {
  font-weight: 700;
  font-size: 32px;
  line-height: 44px;
  color: #04103B;
}
</style>