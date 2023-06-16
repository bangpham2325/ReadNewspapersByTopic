<template>
  <div class="media mb-6" style="width: 100%" v-if="userInfo.id">
    <figure class="media-left">
      <p class="image is-64x64">
        <img v-if="userInfo.avatar" :src="userInfo.avatar" class="is-rounded" style="height: 100%" />
        <img v-else src="@/assets/vectors/default_avatar.svg" class="is-rounded" style="height: 100%" />
      </p>
    </figure>

    <div class="media-content">
      <div class="field">
        <p class="control">
        <div class="comment-container">
          <textarea rows="2" autosize v-model="comment" class="textarea" placeholder="Add a comment..."
            @keydown.enter.shift.exact.prevent="" @keydown.enter.exact.prevent="postComment"></textarea>
          <button @click="postComment" class="send-button">
            <font-awesome-icon :icon="['fas', 'paper-plane']" />
          </button>
        </div>
        </p>
      </div>
    </div>
  </div>
  <div v-for="comment in post_comment" :key="comment.id" style="width: 100%">
    <div class="media mb-5">
      <figure class="media-left">
        <p class="image is-64x64 mt-4">
          <img v-if="comment.user.avatar" :src="comment.user.avatar" class="is-rounded" style="height: 100%" />
          <img v-else src="@/assets/vectors/default_avatar.svg" style="height: 100%" />
        </p>
      </figure>

      <div class="media-content">
        <div v-if="edit_id == comment.id" class="field">
          <p class="control">
            <!-- <el-row> -->
              <div class="comment-container">
                <textarea rows="2" autosize v-model="contentEdit" class="textarea" placeholder="Add a comment..."
                  @keydown.enter.shift.exact.prevent=""
                  @keydown.enter.exact.prevent="updateComment(comment.id)"></textarea>
                <button @click="updateComment(comment.id)" class="send-button">
                  <font-awesome-icon :icon="['fas', 'paper-plane']" />
                </button>
              </div>
            <!-- </el-row> -->
          </p>

        </div>

        <div v-else class="content">
          <p v-if="userInfo.id == comment.user.id" class="title is-4 ml-3 mt-3 name-commenter">Bạn</p>
          <p v-else-if="comment.user.id == this.user_post_id" class="title is-4 ml-3 mt-3">Tác giả</p>
          <p v-else class="title is-4 ml-3 mt-3">{{ comment.user.full_name }}</p>
          <p class="subtitle is-5 ml-3 mt-1 comment-content">{{ comment.content }}</p>
          <p>
            <span><el-button text @click="replyComment(comment.id)">Reply</el-button></span>
            <span v-if="userInfo.id == comment.user.id || userInfo.role == ROLES.ADMIN">
              <el-button text @click="editComment(comment.id, comment.content, 'parent')">Edit</el-button>
              <el-button text @click="delComment(comment.id)">Delete</el-button>
            </span>
            <span class="subtitle is-6 time-comment">{{ comment.time_comment }}</span>
          </p>
        </div>

        <div v-if="comment.child_comments.length != 0">
          <div v-for="item in comment.child_comments" :key="item.id" style="width: 100%">
            <div class="media">
              <figure class="media-left">
                <p class="image is-48x48 mt-4">
                  <img v-if="item.user.avatar" :src="item.user.avatar" class="is-rounded" style="height: 100%" />
                  <img v-else src="@/assets/vectors/default_avatar.svg" style="height: 100%" />
                </p>
              </figure>
              <div class="media-content">
                <div v-if="edit_child_id == item.id" class="field">
                  <p class="control">
                    <!-- <el-row> -->
                      <div class="comment-container">
                        <textarea rows="2" autosize v-model="contentEdit" class="textarea" placeholder="Add a comment..."
                          @keydown.enter.shift.exact.prevent=""
                          @keydown.enter.exact.prevent="updateComment(item.id)"></textarea>
                        <button @click="updateComment(item.id)" class="send-button">
                          <font-awesome-icon :icon="['fas', 'paper-plane']" />
                        </button>
                      </div>
                    <!-- </el-row> -->
                  </p>
                </div>

                <div v-else class="content">
                  <p v-if="userInfo.id == item.user.id" class="title is-4 ml-3 mt-3">Bạn</p>
                  <p v-else-if="item.user.id === this.user_post_id" class="title is-4 ml-3 mt-3"> tác giả</p>
                  <p v-else class="title is-4 ml-3 mt-3">{{ item.user.full_name }}</p>
                  <p class="subtitle is-5 ml-3 mt-1">{{ item.content }}</p>
                  <p>
                    <span v-if="userInfo.id == item.user.id || userInfo.role == ROLES.ADMIN">
                      <el-button text @click="editComment(item.id, item.content, 'child')">Edit</el-button>
                      <el-button text @click="delComment(item.id)">Delete</el-button>
                    </span>
                    <span class="subtitle is-6 time-comment">{{ item.time_comment }}</span>
                  </p>
                </div>

              </div>
            </div>
          </div>
        </div>

        <div v-if="open_id == comment.id" style="width: 100%">
          <div class="media">
            <figure class="image is-48x48 mr-2">
              <img v-if="comment.user.avatar" :src="comment.user.avatar" class="is-rounded" style="height: 100%" />
              <img v-else src="@/assets/vectors/default_avatar.svg" class="is-rounded" style="height: 100%" />
            </figure>
            <div class="media-content">
              <div class="field">
                <p class="control">
                  <!-- <el-row style="width: ;"> -->
                    <div class="comment-container">
                      <textarea rows="2" autosize v-model="contentReply" class="textarea" placeholder="Add a comment..."
                        @keydown.enter.shift.exact.prevent=""
                        @keydown.enter.exact.prevent="newReply(comment.id)"></textarea>
                      <button @click="newReply(comment.id)" class="send-button">
                        <font-awesome-icon :icon="['fas', 'paper-plane']" />
                      </button>
                    </div>
                  <!-- </el-row> -->
                </p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>
  
<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { mapActions, mapGetters, mapState } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElNotification } from "element-plus";
import { ROLES } from "@/const/roles";
import Posts from '@/types/post/PostItem';

@Options({
  props: {
    post: [] as Posts[],
  },

  data() {
    return {
      comment: "",
      post_comment: [] as any,
      contentReply: "",
      status: false,
      open_id: "",
      contentEdit: "",
      edit_id: "",
      edit_child_id: "",
      ROLES: ROLES,
      user_post_id: "",
    };
  },
  methods: {
    ...mapActions("discussion", [
      ActionTypes.FETCH_COMMENTS,
      ActionTypes.CREATE_COMMENT,
      ActionTypes.REPLY_COMMENT,
      ActionTypes.UPDATE_COMMENT,
      ActionTypes.REMOVE_COMMENT]),
    ...mapActions("post", [ActionTypes.FETCH_POST_DETAIL]),

    async getPostDetail() {
      let data = await this.FETCH_POST_DETAIL(this.$route.params.slug)
      this.post_comment = data.post_comment
      this.user_post_id = this.post.user.id ? this.post.user.id : ""
    },
    async postComment() {
      if (this.comment) {
        let response = await this.CREATE_COMMENT({
          id: this.post.id,
          content: this.comment,
        });

        if (response.status == 201) {
          this.comment = ''
          await this.getPostDetail()
        }
      } else {
        ElNotification({
          message: 'Vui lòng ghi bình luận của bạn!',
          type: 'warning',
        })
      }
    },
    replyComment(id: string) {
      this.open_id = id
      this.contentReply = ''
    },
    async newReply(id: string) {
      if (this.contentReply) {
        await this.REPLY_COMMENT({
          post_id: this.post.id,
          content: { content: this.contentReply, parent_comment_id: id },
        }),
          this.contentReply = ''
        await this.getPostDetail()
      } else {
        ElNotification({
          message: 'Vui lòng ghi bình luận của bạn!',
          type: 'warning',
        })
      }
    },
    editComment(id: string, content: string, object: string) {
      if (object == 'parent') {
        this.edit_id = id
      } else {
        this.edit_child_id = id
      }
      this.contentEdit = content
    },
    async updateComment(id: string) {
      if (this.contentEdit) {
        await this.UPDATE_COMMENT({
          post_id: this.post.id,
          comment_id: id,
          content: { content: this.contentEdit },
        }),
          this.contentEdit = '',
          this.edit_child_id = '',
          this.edit_id = ''
        await this.getPostDetail()
      } else {
        ElNotification({
          message: 'Vui lòng ghi bình luận của bạn!',
          type: 'warning',
        })
      }
    },

    async delComment(id: string) {
      const response = await this.REMOVE_COMMENT({
        post_id: this.post.id,
        comment_id: id,
      })
      if (response.status == 204) {
        await this.getPostDetail(),
          ElNotification({
            message: 'Your comment is removed!',
            type: 'success',
          })
      }
    }
  },

  computed: {
    ...mapGetters("user", ["userInfo"]),
    ...mapState("user", ["userInfo"])
  },

  watch: {
    async post() {
      await this.getPostDetail()
    }
  },

  async created() {
    this.unwatchComment = this.$watch('post', (newVal: any) => {
      if (newVal) {
        this.post_comment = { ...newVal.post_comment }
        this.unwatchComment();
      }
    });
  }
})
export default class CommentSection extends Vue {
}
</script>
  
<style scoped>
.media {
  margin-top: 12px !important;
}

.control {
  position: relative;
}

.btn-comment {
  border: none;
  margin-top: 15px;
  position: absolute;
  right: 0;
  padding: 5px 10px;
  cursor: pointer;
  background-color: #00773e;
  color: white;
  border-radius: 5px;
  transition: background-color 0.2s ease-in;
  min-width: 150px;
}

.btn-comment:hover {
  background-color: #008c48;
}

.btn-container-reply {
  position: relative;
  width: 100%;
  height: 20px;
}

.btn-container-edit {
  position: relative;
  width: 100%;
  height: 40px;
}

.btn-reply,
.btn-edit {
  font-size: 1rem;
  position: absolute;
  right: 0;
}

.content {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 10px;
  cursor: default;
}

.content p {
  margin: 0;
}

.content p {
  margin: 0;
}

.comment-content {
  font-size: 1rem;
}

.time-comment {
  position: absolute;
  right: 20px;
  top: 28px;
}

.el-button.is-text {
  margin: 0;
}

.el-button.is-text {
  padding-left: 12px;
  padding-right: 12px;

}

.comment-container {
  position: relative;
}

.send-button {
  position: absolute;
  bottom: 2px;
  right: 10px;
  background-color: transparent;
  border: 0;
}
</style>