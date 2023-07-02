<template>
  <el-main>
    <el-table
      highlight-current-row
      :data="users"
      v-loading="loading"
      stripe
      size="large"
    >
      <el-table-column type="index" sortable label="#" align="center" width="80"/>
      <el-table-column prop="avatar" align="center" label="Avatar" width="150">
        <template #default="scope">
          <div>
            <el-avatar v-if="scope.row.avatar" :size="50" :src="scope.row.avatar" />
            <el-avatar v-else :size="50">
              <img src="@/assets/vectors/default_avatar.svg" alt="User Avatar">
            </el-avatar>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="full_name" sortable label="Name" min-width="250"/>
      <el-table-column prop="role" sortable label="Role" width="150"/>
      <el-table-column prop="email" sortable label="Email" width="350"/>
      
    </el-table>

    <Pagination
      :total="total"
      :page="query.page"
      :page_size="query.page_size"
      @changePage="$emit('changePage', $event)">
    </Pagination>
  </el-main>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import Pagination from "@/components/Pagination.vue";

@Options({
  props: {
    users: {
      type: Array,
      default: [
        {
          id: "",
          full_name: "",
          role: "",
          avatar: "",
          email: "",
        } as any
      ]
    },
    total: 0,
    query: {
      page: 1,
      page_size: 12,
      q: "",
      role: ""
    },
    loading: false,
  },
  components: {
    Pagination
  },
  data() {
    return {
    }
  }
})
export default class UserSection extends Vue {
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap');

.user-record {
  background: #FFFFFF;
  border: 1px solid #EBE8FF;
  border-radius: 15px;
}

p {
  font-family: 'Nunito';
  font-weight: 600;
  font-size: 14px;
  line-height: 19px;
  color: #797D8C;
}

h1 {
  font-family: 'Nunito';
  font-style: normal;
  font-weight: 800;
  font-size: 16px;
  line-height: 22px;
  display: flex;
  color: #04103B;
  mix-blend-mode: normal;
}

h2 {
  font-style: normal;
  font-weight: 600;
  font-size: 20px;
  line-height: 30px;
  letter-spacing: 0.02em;
  color: #000000;
  opacity: 0.5;
}

.title {
  background: #dedfe4;
  opacity: 0.75;
  border-radius: 7px;
  font-family: 'Inter';
  font-size: 12px;
  line-height: 15px;
  letter-spacing: 0.02px;
  color: #323c4c;
  text-align: center;
  margin-bottom: 0px !important;
}
</style>