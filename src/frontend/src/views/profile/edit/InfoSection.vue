<template>
  <el-form style="width:100%;" label-width="100px" size="large" v-model="editForm">
    <el-form-item label="Họ và tên">
      <el-input placeholder="Điền họ và tên" v-model="editForm.full_name" />
    </el-form-item>

    <el-form-item label="Email">
      <el-input placeholder="Điền email" disabled v-model="editForm.account.email" />
    </el-form-item>

    <el-form-item label="Địa chỉ">
      <el-input placeholder="Điền địa chỉ" v-model="editForm.address" />
    </el-form-item>

    <el-form-item label="Ngày sinh">
      <el-date-picker v-model="editForm.birthday" type="date" placeholder="Chọn ngày tháng năm sinh" style="width: 100%"
        format="DD/MM/YYYY" value-format="YYYY-MM-DD" />
    </el-form-item>

    <el-form-item label="Giới thiệu">
      <el-input placeholder="Giới thiệu về bản thân" type="textarea" v-model="editForm.bio" />
    </el-form-item>

    <el-form-item label="Chủ đề">
      <el-tag v-for="topic in userInfo.categories" :key="topic" class="ml-2" type="warning">{{ topic.title }}</el-tag>
      <el-button type="warning" plain class="ml-2" size="small" @click="changeTopic">
        + Thay đổi</el-button>
    </el-form-item>

    <el-form-item>
      <el-button type="success" round @click="onSubmit">Cập nhật</el-button>
      <el-button type="info" round @click="gotoPW">Thay đổi mật khẩu</el-button>
      <el-button round @click="$router.go(-1)">Hủy bỏ</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapGetters } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElNotification } from 'element-plus'

@Options({
  props: {
    user: {} as any,
    editForm: {
      account: {
        email: ""
      }
    } as any,
  },
  data() {
    return {
      avatar: null
    }
  },
  methods: {
    ...mapActions("user", [ActionTypes.UPDATE_USER_PROFILE, ActionTypes.GET_USER_PROFILE]),

    async getProfileDetail() {
      let response: any = await this.GET_USER_PROFILE(this.tokenInfo.user_id);
      if (response.status == 200) {
        this.editForm = response.data;
      }
    },

    async onSubmit() {
      this.avatar = this.editForm.avatar
      delete this.editForm["avatar"]
      const response = await this.UPDATE_USER_PROFILE({
        user_id: this.tokenInfo.user_id,
        data: this.editForm
      })
      if (response.status == 200) {
        ElNotification({
          title: 'Update successfully',
          message: "You've just updated your information.",
          type: 'success',
        })
        this.editForm["avatar"] = this.avatar
      }
      else {
        ElNotification({
          title: 'Error',
          message: 'Information is incorrect. Please check again',
          type: 'error',
        })
      }
    },

    gotoPW(){
      this.$router.push("/change-password")
    },

    changeTopic(){
      this.$router.push("/category")
    }
  },
  computed: {
    ...mapGetters("authentication", ["tokenInfo"]),
    ...mapGetters("user", ["userInfo"]),
  },
})

export default class InfoSection extends Vue {
  editForm!: any
}
</script>

<style>

</style>