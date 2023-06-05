<template>
  <h2 class="title is-2 mt-6">BÌNH LUẬN</h2>
  
  <div class="media mb-6" style="width: 100%" v-if="userInfo.id">
    <figure class="media-left">
			<p class="image is-64x64">
				<img v-if="userInfo.avatar" :src="userInfo.avatar" class="is-rounded" style="height: 100%"/>
				<img v-else src="@/assets/vectors/default_avatar.svg" class="is-rounded" style="height: 100%"/>
			</p>
    </figure>
  
		<div class="media-content">
			<div class="field">
				<p class="control">
					<textarea
						rows="3"
						autosize
						v-model="comment"
						class="textarea"
						placeholder="Add a comment..."
						@keydown.enter.shift.exact.prevent=""
						@keydown.enter.exact.prevent="postComment"
					></textarea>
				</p>
			</div>
		</div>
  </div>
  
	<div
		v-for="comment in post_comment"
		:key="comment.id"
		style="width: 100%"
	>
		<div class="media mb-5">
			<figure class="media-left">
				<p class="image is-64x64 mt-4">
					<img v-if="comment.user.avatar" :src="comment.user.avatar" class="is-rounded" style="height: 100%"/>
					<img v-else src="@/assets/vectors/default_avatar.svg" style="height: 100%"/>
				</p>
			</figure>
  
			<div class="media-content">
				<div v-if="edit_id == comment.id" class="field">
					<p>
						<el-row>
              <textarea
                rows="2"
                autosize
                v-model="contentEdit"
                class="textarea"
                placeholder="Add a comment..."
                @keydown.enter.shift.exact.prevent=""
                @keydown.enter.exact.prevent="updateComment(comment.id)"
              ></textarea>
						</el-row>
					</p>
					
				</div>
  
				<div v-else class="content">
					<p class="title is-4 ml-3 mt-3">{{ comment.user.full_name }}</p>
					<p class="subtitle is-5 ml-3 mt-1">{{ comment.content }}</p>
					<p>
						<span><el-button text @click="replyComment(comment.id)">Reply</el-button></span>
						<span v-if="userInfo.id == comment.user.id || userInfo.role == ROLES.ADMIN">
							<el-button text @click="editComment(comment.id, comment.content, 'parent')">Edit</el-button>
							<el-button text @click="delComment(comment.id)">Delete</el-button>
						</span>
						<span class="subtitle is-6">{{ comment.time_comment }}</span>
					</p>
				</div>
  
				<div v-if="comment.child_comments.length != 0">
					<div
						v-for="item in comment.child_comments"
						:key="item.id"
						style="width: 100%"
					>
						<div class="media">
							<figure class="media-left">
								<p class="image is-48x48 mt-4">
									<img v-if="item.user.avatar" :src="item.user.avatar" class="is-rounded" style="height: 100%"/>
									<img v-else src="@/assets/vectors/default_avatar.svg" style="height: 100%"/>
								</p>
							</figure>
							<div class="media-content">
								<div v-if="edit_child_id == item.id" class="field">
									<p>
										<el-row>
												<textarea
													rows="2"
													autosize
													v-model="contentEdit"
													class="textarea"
													placeholder="Add a comment..."
                          @keydown.enter.shift.exact.prevent=""
                          @keydown.enter.exact.prevent="updateComment(item.id)"
												></textarea>
										</el-row>
									</p>
								</div>

								<div v-else class="content">
                  <p class="title is-4 ml-3 mt-3">{{ item.user.full_name }}</p>
					        <p class="subtitle is-5 ml-3 mt-1">{{ item.content }}</p>
									<p>
										<span v-if="userInfo.id == item.user.id || userInfo.role == ROLES.ADMIN">
											<el-button text @click="editComment(item.id, item.content, 'child')">Edit</el-button>
											<el-button text @click="delComment(item.id)">Delete</el-button>
										</span>
                    <span class="subtitle is-6">{{ item.time_comment }}</span>
									</p>
								</div>

							</div>
						</div>
          </div>
        </div>
  
			<div v-if="open_id == comment.id" style="width: 100%">
				<div class="media">
					<figure class="image is-48x48 mr-2">
						<img v-if="comment.user.avatar" :src="comment.user.avatar" class="is-rounded" style="height: 100%"/>
						<img v-else src="@/assets/vectors/default_avatar.svg" class="is-rounded" style="height: 100%"/>
					</figure>
					<div class="media-content">
						<div class="field">
							<p>
								<el-row>
                  <textarea
                    rows="2"
                    autosize
                    v-model="contentReply"
                    class="textarea"
                    placeholder="Add a comment..."
                    @keydown.enter.shift.exact.prevent=""
                    @keydown.enter.exact.prevent="newReply(comment.id)"
                  ></textarea>
								</el-row>
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
  import {Options, Vue} from "vue-class-component";
  import {mapActions, mapGetters, mapState} from "vuex";
  import {ActionTypes} from "@/types/store/ActionTypes";
  import {ElNotification} from "element-plus";
  import {ROLES} from "@/const/roles";
  
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

      async getPostDetail(){ 
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
            content: {content: this.contentReply, parent_comment_id: id},
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
            content: {content: this.contentEdit},
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
      this.unwatchComment = this.$watch('post', (newVal:any) => {
        if (newVal) {
          this.post_comment = {...newVal.post_comment}
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
  </style>