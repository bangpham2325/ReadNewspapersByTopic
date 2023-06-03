<template>
  <el-row>
	<el-col :span="12">
      <el-tag class="mr-4" size="large" v-for="tag in this.postDetail.keywords">{{ tag.keyword }}</el-tag>
    </el-col>
    <el-col :span="12">
      <el-row class="is-flex is-justify-content-right" v-if="postDetail.status=='PUBLISHED'">
        <el-button v-if="!this.postDetail.has_bookmarked" type="text" icon="Collection" style="color:#00773e;" size="large" @click="actionPost('save')">Lưu bài</el-button>
        <el-button v-else type="text" icon="Management" style="color:#FF9900;" size="large" @click="actionPost('unsave')">Bỏ lưu</el-button>
        <el-tooltip content="Thích bài viết" placement="top-start">
          <el-button v-if="!this.postDetail.has_liked" type="text" icon="Star" style="color:#00773e;" size="large" @click="actionPost('like')">{{ postDetail.likes }}</el-button>
          <el-button v-else type="text" icon="StarFilled" style="color:#FF9900;" size="large" @click="actionPost('unlike')">{{ postDetail.likes }}</el-button>
        </el-tooltip>
		<el-tooltip content="Đánh giá bài viết" placement="top-start">
			<el-button type="text" icon="ChatRound" style="color:#00773e;" size="large" @click="ratingSection=true">{{ postDetail.total_rating }}</el-button>
		</el-tooltip>
		<button v-if="this.userInfo.role === 'ADMIN'" class="button is-dark" @click="statusPost('DRAFT')">Ẩn bài viết</button>
      </el-row>

	  <el-row v-else class="is-flex is-justify-content-right">
		<button class="button is-primary" style="background-color: #00773e;" @click="statusPost('PUBLISHED')">Đăng bài viết</button>
	  </el-row>
    
      <el-dialog v-model="ratingSection">
        <form>
          <div class="field">
            <label class="title is-4">Đánh giá sự hài lòng của bạn về bài viết:</label>
            <div class="control mt-5">
              <div class="rating-stars">
                <el-rate
                  v-model="rating"
                  :max="5"
                  :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                ></el-rate>
              </div>
            </div>
          </div>
          
          <div class="field">
            <div class="control">
              <input class="input" type="text" v-model="title" placeholder="Chủ đề">
            </div>
          </div>
    
          <div class="field">
            <div class="control">
              <textarea class="textarea" v-model="feedback" placeholder="Viết nhận xét của bạn tại đây"></textarea>
            </div>
          </div>
      
          <div class="field">
            <div class="control">
              <button class="button is-black" @click="submitRatingForm">Submit</button>
            </div>
          </div>
        </form>
      </el-dialog>
    </el-col>
  </el-row>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapState, mapGetters, mapMutations} from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';
import {ElMessage} from "element-plus";

@Options({
	computed: {
    ...mapState(["is_loading"]),
    ...mapGetters("user", ["userInfo"]),
  },

	props: {
		postDetail: {},
	},

	data() {
		return {
			ratingSection: false,
			rating: 0,
			feedback: "",
			title: "",
			has_rating: false,
		}
	},

	methods: {
		...mapMutations(["SET_LOADING"]),
    ...mapActions("post", [ActionTypes.ADD_POST_BOOKMARK, ActionTypes.LIKE_POST, ActionTypes.RATE_POST, ActionTypes.UPDATE_STATUS_POST]),

		async actionPost(action: String){
			if(this.userInfo.id){
				if(action == "save"){
					let res = await this.ADD_POST_BOOKMARK(this.postDetail.id)
					if (res.status == 200) {
						ElMessage({
							message: `Lưu ${this.postDetail.title} thành công.`,
							type: 'success',
						})

						this.postDetail.has_bookmarked = true
					} 
					else {
						ElMessage.error('Đã có lỗi xảy ra.')
					}
				}
				else if(action == "unsave"){
					let res = await this.ADD_POST_BOOKMARK(this.postDetail.id)
					if (res.status == 200) {
						ElMessage({
							message: `Bỏ lưu ${this.postDetail.title} thành công.`,
							type: 'success',
						})

						this.postDetail.has_bookmarked = false
					} 
					else {
						ElMessage.error('Đã có lỗi xảy ra.')
					}
				}
				else if(action == "like"){
					let res = await this.LIKE_POST(this.postDetail.id)
					if (res.status == 200) {
						this.postDetail.has_liked = true
						this.postDetail.likes = res.data.likes
					}
				}
				else if(action == "unlike"){
					let res = await this.LIKE_POST(this.postDetail.id)
					if (res.status == 200) {
						this.postDetail.has_liked = false
						this.postDetail.likes = res.data.likes
					}
				}

			}
			else {
				this.$router.push("/login")
			}
		},

		async submitRatingForm(){
      if(this.userInfo.id){
        let res = await this.RATE_POST({
          id: this.postDetail.id,
          feedback: {
            title: this.title,
            content: this.feedback,
            star_rating: this.rating
          }
        })
      }
      else {
				this.$router.push("/login")
			}
		},

		async statusPost(status:string){
			let res = await this.UPDATE_STATUS_POST({id: this.postDetail.id, status: {status: status}})
			if (res.status == 200){
				window.location.reload();
				if(status == 'PUBLISHED')
					ElMessage({
						message: `Đăng bài ${this.postDetail.title} thành công.`,
						type: 'success',
					})
				else
				ElMessage({
					message: `Ẩn bài ${this.postDetail.title} thành công.`,
					type: 'success',
				})
			}
			else{
				ElMessage.error('Đã có lỗi xảy ra.')
			}
		}
	},
	created(){
		for ( let rate in this.postDetail.post_rating){
			if(this.postDetail.post_rating[rate].id == this.userInfo.id)
				this.has_rating = true
		}
	}
})

export default class FooterSection extends Vue {
}
</script>

<style scoped>
.rating-stars {
  display: inline-block;
  margin-bottom: 0.5rem;
  width: 100%;
}
.el-rate {
	--el-rate-icon-size: 60px;
}

</style>