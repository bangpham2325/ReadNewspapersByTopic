<template>
  <div class="rating-section">
    <div v-for="rating in post.post_rating" :key="rating.id" class="rating-item">
      <div class="rating-info">
        <div class="avatar">
          <img class="is-rounded" v-if="rating.user.avatar" :src="rating.user.avatar" alt="User Avatar">
          <img v-else src="@/assets/vectors/default_avatar.svg" alt="Default Avatar">
        </div>
        <div class="rating-details">
          <!-- <h3 class="rating-title">Title: {{ rating.title }}</h3> -->
          <div class="rating-meta">
            <span class="user-name">{{ rating.user.full_name }}</span>
            <span class="date">{{ rating.time_rating }}</span>
          </div>
        </div>
      </div>
      <a-rate class="star-rating" :value="rating.star_rating" />
      <p class="rating-content">{{ rating.title }}</p>
    </div>
  </div>
</template>
  
<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { mapActions, mapGetters, mapState } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElNotification } from "element-plus";
import { ROLES } from "@/const/roles";

@Options({
  props: {
    post: [] as any
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
      ROLES: ROLES
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
      let data = await this.FETCH_POST_DETAIL(this.$route.params.id)
      this.post_comment = data.post_comment
    },
    async postComment() {
      if (this.comment) {
        let response = await this.CREATE_COMMENT({
          id: this.$route.params.id,
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
          post_id: this.$route.params.id,
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
          post_id: this.$route.params.id,
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
        post_id: this.$route.params.id,
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
export default class RatingSection extends Vue {
}
</script>
  
<style scoped>
.rating-section {
  margin-top: 30px;
}

.rating-item {
  background-color: #f9f9f9;
  border: 1px solid #eaeaea;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 20px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.rating-info {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.rating-details {
  margin-left: 10px;
}

.rating-title {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.rating-meta {
  display: flex;
  align-items: center;
}

.user-name {
  font-weight: bold;
  margin-right: 5px;
}

.date {
  font-style: italic;
  color: #666;
}

.star-rating {
  margin-bottom: 10px;
}

.rating-content {
  margin: 0;
  color: #666;
}

@media (max-width: 768px) {
  .rating-item {
    padding: 15px;
  }

  .avatar {
    width: 40px;
    height: 40px;
  }

  .rating-title {
    font-size: 16px;
  }
}
</style>