<template>
  <el-tooltip
    class="box-item"
    effect="dark"
    content="Click here to change background"
    placement="top"
    :disabled="is_freeze"
  >
    <el-upload
      class="avatar-uploader"
      action=""
      :on-change="changeFile"
      :show-file-list="false"
      :before-upload="beforeImageUpload"
      :on-success="handleImageUpload"
      :on-error="handleImageUpload"
      :disabled="is_freeze"
    >
      <img v-if="image" :src="image" class="avatar" />
      <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
    </el-upload>
  </el-tooltip>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { ElNotification } from "element-plus";

@Options({
  props: {
    image: null,
    is_freeze: false
  },
  methods: {
    changeFile(file: any, fileList: any) {
      this.$emit('change-file', file)
    },
    handleImageUpload(res: any, file: any) {
      this.$emit('change-image', URL.createObjectURL(file.raw))
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
    }
  }
})

export default class CoverImage extends Vue {
  image!: any;
  is_freeze!: boolean
}
</script>

<style scoped>
.avatar-uploader .avatar {
  width: 100%;
  border-radius: 20px;
  object-fit: cover;
  aspect-ratio: 21/9;
  display: block;
}

:deep(.el-upload) {
  border-radius: 20px;
  display: block;
  aspect-ratio: 21/9;
  box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
  transition: all 0.2s linear;
}

:deep(.el-upload:hover) {
  opacity: 0.9;
}
</style>

<style lang="scss" scoped>
.avatar-uploader .el-upload {
  border-radius: 20px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 100%;
  aspect-ratio: 21/9;
  transition: var(--el-transition-duration-fast);
}

.el-icon.avatar-uploader-icon {
  border-radius: 20px;
  background-color: #eee;
  font-size: 28px;
  color: #8c939d;
  width: 100%;
  height:100%;
  margin: 0 auto;
}

</style>