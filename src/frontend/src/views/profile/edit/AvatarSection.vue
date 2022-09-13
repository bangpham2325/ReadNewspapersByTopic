<template>
  <div class="columns has-background-white m-3 p-3 is-flex is-vcentered" style="border-radius: 20px">
    <div class="column is-flex is-justify-content-center is-one-fifth">
      <el-tooltip class="box-item" effect="dark" content="Click here to change your avatar" placement="top">
        <el-upload class="avatar-uploader" action="" :http-request="updateAvatar" :show-file-list="false"
          :on-change="changeFile" :before-upload="beforeImageUpload" :disabled="is_freeze">
          <figure class="image is-128x128">
            <img v-if="user.avatar" :src="user.avatar" class="is-rounded" style="height: 100%">
            <img v-else src="@/assets/vectors/default_avatar.svg" class="is-rounded" style="height: 100%" />
          </figure>
        </el-upload>
      </el-tooltip>
    </div>
    <div class="column">
      <p class="title is-4 is-capitalized">{{ user.full_name }}</p>
      <p class="subtitle is-6 is-italic is-capitalized">{{ user.role.toLowerCase() }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapState } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElNotification } from 'element-plus'

@Options({
  props: {
    user: {} as any
  },
  data() {
    return {
      avatar: null,
      is_freeze: false,
    }
  },
  methods: {
    ...mapActions("user", [ActionTypes.UPDATE_USER_PROFILE, ActionTypes.GET_USER_INFO]),

    changeFile(file: any, fileList: any) {
      this.avatar = file;
      this.$emit('change-avatar', URL.createObjectURL(file.raw))
    },

    beforeImageUpload(file: any) {
      const isJPG = file.type === "image/jpeg";
      const isPNG = file.type === "image/png";
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG && !isPNG) {
        ElNotification({
          title: 'Notice',
          message: 'Avatar picture must be JPG or PNG format!',
          type: 'info',
        })
      }
      if (!isLt2M) {
        ElNotification({
          title: 'Notice',
          message: 'Avatar picture size can not exceed 2MB!',
          type: 'info',
        })
      }
      return (isJPG || isPNG) && isLt2M;
    },

    async updateAvatar() {
      let formData = new FormData();

      formData.append("avatar", this.avatar.raw);

      const response = await this.UPDATE_USER_PROFILE({
        user_id: this.user.id,
        data: formData
      })

      if (response.status == 200) {
        await this.GET_USER_INFO(this.tokenInfo.user_id)
        ElNotification({
          title: 'Update successfully',
          message: "You've just updated your avatar.",
          type: 'success',
        })
      }
    }
  },
  computed: {
    ...mapState("authentication", ["tokenInfo"])
  }
})

export default class AvatarSection extends Vue {
  user!: any
}
</script>

<style scoped>
.avatar-uploader .el-upload {
  border-radius: 20px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 100% !important;
  aspect-ratio: 21/9;
  transition: var(--el-transition-duration-fast);
}

.el-icon.avatar-uploader-icon {
  border-radius: 20px;
  background-color: #eee;
  font-size: 28px;
  color: #8c939d;
  width: 100%;
  height: 100%;
  margin: 0 auto;
}
</style>
