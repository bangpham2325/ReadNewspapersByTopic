<template>
	<el-tooltip :content=postDetail.publish_date placement="top-start">
		<p class="title is-6" style="color:#808080">{{ postDetail.publish_date }}</p>
	</el-tooltip>

	<p class="title is-5" style="color:#00773e">{{ postDetail.category.title }}</p>
	<h1 class="title is-2">{{ postDetail?.title }}</h1>
	<p class="subtitle is-5" style="color:#808080">{{ postDetail.summary }}</p>
	
	<el-row>
		<el-col :span="12">
			<el-row>
					<el-avatar :size="50">
						<img src="https://img.vietcetera.com/uploads/avatar-images/12-apr-2023/vu-hoang-long-1681282620604-160x160.jpg">
					</el-avatar>
					<p class="title is-6 mt-4 ml-4" style="color:#00773e;">{{ postDetail.author }}</p>
			</el-row>
		</el-col>

		<el-col :span="12">
			<el-row class="is-flex is-justify-content-right">
				<el-button v-if="!this.postDetail.has_bookmarked" type="text" icon="CollectionTag" style="color:#00773e;" size="large" @click="actionPost('save')">Lưu bài</el-button>
				<el-button v-else type="text" icon="CollectionTag" style="color:#00773e;" size="large" @click="actionPost('unsave')">Bỏ lưu</el-button>
				<el-button type="text" icon="View" style="color:#00773e;" size="large">{{ postDetail.views }}</el-button>
				<el-tooltip content="Like" placement="top-start">
					<el-button v-if="!this.postDetail.has_liked" type="text" icon="Star" style="color:#00773e;" size="large" @click="actionPost('like')">{{ postDetail.likes }}</el-button>
					<el-button v-else type="text" icon="StarFilled" style="color:#00773e;" size="large" @click="actionPost('unlike')">{{ postDetail.likes }}</el-button>
				</el-tooltip>
				<el-button type="text" icon="ChatRound" style="color:#00773e;" size="large" @click="ratingSection=true">{{ postDetail.total_rating }}</el-button>
			</el-row>
		</el-col>

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
			bookmark_id: "",
			ratingSection: false,
			rating: 0,
			feedback: "",
			title: "",
			has_rating: false,
		}
	},

	methods: {
		...mapMutations(["SET_LOADING"]),
    ...mapActions("post", [ActionTypes.ADD_POST_BOOKMARK, ActionTypes.LIKE_POST, ActionTypes.RATE_POST]),

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
			let res = await this.RATE_POST({
				id: this.postDetail.id,
				feedback: {
					title: this.title,
					content: this.feedback,
					star_rating: this.rating
				}
			})
		}
	},
	created(){
		for ( let rate in this.postDetail.post_rating){
			if(this.postDetail.post_rating[rate].id == this.userInfo.id)
				this.has_rating = true
		}
	}
})

export default class SummarySection extends Vue {
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