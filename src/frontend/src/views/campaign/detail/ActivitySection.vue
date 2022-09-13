<template>
  <div
    class="has-background-white"
  >
    <div class="p-2" style="border: 1px dashed #ccc; border-radius: 4px" v-show="isAuth">
      <button
        :class="['button', 'is-light', {'mb-3': newPost}]"
        style="width: 100%; font-weight: 500"
        @click="newPost =! newPost"
      >
        {{ newPost ? 'Hide' : 'Update New Activity' }}
      </button>
      <el-form
        ref="formRef"
        label-position="top"
        label-width="100px"
        :model="post"
        size="large"
        :disabled="is_freeze"
        :rules="rules"
        v-show="newPost"
      >
        <el-form-item prop="title">
          <el-input v-model="post.title" placeholder="Title"/>
        </el-form-item>

        <el-form-item prop="description">
          <el-input v-model="post.description" type="textarea" placeholder="Tell something about this campaign..."/>
        </el-form-item>

        <el-upload
          ref="upload"
          class="upload-demo"
          action=""
          :limit="10"
          :auto-upload="false"
          :file-list="fileList"
          :on-change="cert_path_file"
        >
          <template #trigger>
            <el-button type="primary" size="default">Add images</el-button>
          </template>
          <template #tip>
            <div class="el-upload__tip text-red">
              limit 10 files
            </div>
          </template>
        </el-upload>

        <div class="is-flex is-justify-content-end">
          <button
            class="button"
            @click.prevent="handleSubmit($refs.formRef)"
            :disabled="is_freeze">
            <el-icon v-if="is_freeze" class="is-loading mr-2">
              <Loading/>
            </el-icon>
            Post
          </button>
        </div>
      </el-form>
    </div>
    <div
      v-for="post in campaign.post_events"
      :key="post.id"
      class="mt-5"
    >
      <PostItem
        :post="post"
        :event_id="campaign.id"
        :registerStatus="registerStatus"
        @addComment="addComment(post.id, $event)"
      ></PostItem>
    </div>
    <div v-if="campaign.post_events.length == 0" class="mt-3">
      No activity here.
    </div>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from "vue-class-component";
import {ElNotification, FormInstance} from "element-plus";
import {CAMPAIGN_STATUS} from "@/const/campaign_status";
import {mapActions, mapGetters} from "vuex";
import {ActionTypes} from "@/types/store/ActionTypes";
import PostItem from "@/views/campaign/detail/components/PostItem.vue";
import {PROCESS_STATUS} from "@/const/process_status";

@Options({
  components: {
    PostItem
  },
  props: {
    registerStatus: {
      type: String,
      default: PROCESS_STATUS.UNREGISTER
    },
    campaign: {
      type: Object,
      default: {
        id: "",
        post_events: [
          {
            "id": "",
            "title": "",
            "description": "",
            "images": []
          }
        ],
        user: {
          full_name: ""
        }
      }
    },
    isAuth: false
  },
  methods: {
    ...mapActions("campaign", [ActionTypes.CREATE_CAMPAIGN_POST]),
    addComment(post_id: string, cmt: any){
      let post_index = this.campaign.post_events.map((e: any) => e.id).indexOf(post_id)
      this.campaign.post_events[post_index].comments.unshift(cmt)
    },
    cert_path_file(file: any, fileList: any) {
      this.fileList = fileList;
    },
    async handleSubmit(formEl: FormInstance | undefined) {
      if (!formEl) return
      await formEl.validate(async (valid, fields) => {
        this.is_freeze = true

        if (valid) {
          let formData = new FormData();

          formData.append("title", this.post.title);
          formData.append("description", this.post.description);

          this.fileList.map((img: any) => {
            formData.append("image_events", img.raw)
          })

          const response: any = await this.CREATE_CAMPAIGN_POST({
            id: this.campaign.id,
            form: formData
          })

          if (response.status == 201) {
            this.fileList = ""
            this.post.title = ""
            this.post.description = ""
            let data = {...response.data}
            data.comments = []
            this.$emit('addPost', data)
            ElNotification({
              title: 'Add new activity successfully',
              message: 'Your post is publish for everyone now!',
              type: 'success',
            })
          } else {
            ElNotification({
              title: 'Error',
              message: 'Add new activity failed!',
              type: 'error',
            })
          }
        } else {
          ElNotification({
            title: 'Missing info',
            message: 'Please fill in all required field!',
            type: 'warning',
          })
        }
        this.is_freeze = false
      })
    },
  },
  data() {
    return {
      PROCESS_STATUS: PROCESS_STATUS,
      post: {
        title: "",
        description: "",
      },
      fileList: [],
      newPost: false,
      is_freeze: false,
      rules: {
        title: [
          {required: true, message: 'Please input title', trigger: 'blur'},
          {min: 5, max: 100, message: 'Length should be 5 to 100', trigger: 'blur'},
        ],
        description: [
          {required: true, message: 'Please input description for this post', trigger: 'blur'},
          {min: 5, max: 200, message: 'Length should be 20 to 200', trigger: 'blur'},
        ]
      }
    }
  }
})

export default class ActivitySection extends Vue {
}

</script>

<style>

</style>