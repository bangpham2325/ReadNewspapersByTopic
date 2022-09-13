<template>
  <div class="post-item">
    <div class="p-3">
      <p class="is-flex is-justify-content-space-between">
        <strong>{{ post.title }}</strong>
        <span v-if="post.created_at" class="tag is-medium is-light" style="font-size: 0.8rem">{{ post.created_at.substring(0, 10) }}</span>
      </p>
      <p class="is-size-6 mt-3" style="border-radius: 4px">
        {{ post.description }}
      </p>

      <el-carousel
        :interval="4000"
        v-if="post.images.length > 0"
        arrow="always"
        class="mt-5"
      >
        <el-carousel-item v-for="(img, index) in post.images" :key="img.id">
          <div class="item">
            <el-image
              :src="img.url"
              :initial-index="4"
              fit="cover"
              style="width: 100%"
            />
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>


    <div class="has-background-light p-3">
      <textarea
        rows="1"
        autosize
        v-if="registerStatus == PROCESS_STATUS.REGISTERED"
        v-model="input"
        class="textarea mb-4"
        placeholder="Press enter to reply, shift+enter to add new line"
        @keydown.enter.shift.exact.prevent=""
        @keydown.enter.exact.prevent="postComment"
      ></textarea>

      <div v-for="cmt in post.comments" :key="cmt.id">
        <div class="columns is-flex is-vcentered">
          <div class="column" style="max-width: 80px">
            <figure class="media-left">
              <p class="image is-64x64">
                <img v-if="cmt.user.avatar" :src="cmt.user.avatar" class="is-rounded" style="height: 100%"/>
                <img v-else src="@/assets/vectors/default_avatar.svg" class="is-rounded" style="height: 100%"/>
              </p>
            </figure>
          </div>
          <div class="column is-full">
            <p class="has-background-white p-2" style="width: fit-content; border-radius: 10px; font-size: 1rem">
              {{ cmt.content }}
            </p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>
<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {ElNotification} from "element-plus";
import {mapActions} from "vuex";
import {ActionTypes} from "@/types/store/ActionTypes";
import {PROCESS_STATUS} from "@/const/process_status";

@Options({
  props: {
    registerStatus: {
      type: String,
      default: PROCESS_STATUS.UNREGISTER
    },
    event_id: "",
    post: {
      type: Object,
      default: {
        "id": "",
        "title": "",
        "description": "",
        "images": [
          {
            "id": "",
            "url": "",
            "post_event_id": ""
          }
        ],
        "comments": [
          {
            "id": "",
            "content": "",
            "user": {
              "full_name": "",
              "avatar": ""
            },
          }
        ],
      }
    }
  },
  data() {
    return {
      PROCESS_STATUS: PROCESS_STATUS,
      srcList: [],
      input: ""
    }
  },
  methods: {
    ...mapActions("campaign", [ActionTypes.CREATE_CAMPAIGN_POST_COMMENT]),
    async postComment() {
      if (this.input) {
        let response = await this.CREATE_CAMPAIGN_POST_COMMENT({
          event_id: this.event_id,
          post_id: this.post.id,
          comment: {
            content: this.input
          },
        });

        if (response.status == 201) {
          this.$emit('addComment', response.data)
          this.input = ""
          ElNotification({
            message: 'Your comment is posted!',
            type: 'success',
          }),
            this.comment = '',
            await this.getLesson(this.course.id, this.lesson.chapter_id, this.lesson.id)
        }
      } else {
        ElNotification({
          message: 'Please write your comment!',
          type: 'warning',
        })
      }
    },
  }
})

export default class PostItem extends Vue {
}
</script>

<style lang="scss" scoped>
.post-item {
  border-radius: 4px;
  border: 1px solid #eee;
}
</style>

<style scoped>
.el-carousel__item {
  border-radius: 4px;
}

.item {
  position: relative;
  height: 100%;
}

.item__content {
  position: absolute;
  bottom: 0;
  width: 100%;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  padding: 3px;
}

.item__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
