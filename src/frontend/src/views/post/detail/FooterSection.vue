<template>
	<el-row>
		<el-col :span="12">
			<el-tag class="mr-4" size="large" v-for="tag in this.postDetail.keywords">{{ tag.keyword }}</el-tag>
		</el-col>
		<el-col :span="12">
			<el-row class="is-flex is-justify-content-right" v-if="postDetail.status == 'PUBLISHED'">
				<el-button v-if="!this.postDetail.has_bookmarked" type="text" icon="Collection" style="color:#00773e;"
					size="large" @click="actionPost('save')">Lưu bài</el-button>
				<el-button v-else type="text" icon="Management" style="color:#FF9900;" size="large"
					@click="actionPost('unsave')">Bỏ lưu</el-button>
				<el-tooltip content="Thích bài viết" placement="top-start">
					<el-button v-if="!this.postDetail.has_liked" type="text" size="large" style="color:#00773e;"
						@click="actionPost('like')"><font-awesome-icon :icon="['far', 'thumbs-up']" style="color:#00773e;"
							class="mr-2" />{{ postDetail.likes }}</el-button>
					<el-button v-else type="text" size="large" @click="actionPost('unlike')"
						style="color: #FF9900;"><font-awesome-icon :icon="['fas', 'thumbs-up']" style="color: #FF9900;"
							class="mr-2" />{{ postDetail.likes }}</el-button>
				</el-tooltip>
				<el-tooltip content="Đánh giá bài viết" placement="top-start">
					<el-button type="text" icon="Star" style="color:#00773e;" size="large" @click="ratingSection = true">{{
						postDetail.total_rating }}</el-button>
				</el-tooltip>
			</el-row>
			<div class="modal" :class="{ 'is-active': ratingSection }">
				<div class="modal-background" @click="ratingSection = false"></div>
				<div class="modal-content has-background-white p-6">
					<div class="field">
						<label class="title is-4">Đánh giá sự hài lòng của bạn về bài viết:</label>
						<div class="control mt-5">
							<div class="rating-stars">
								<el-rate v-model="rating" :max="5" :colors="['#99A9BF', '#F7BA2A', '#FF9900']"></el-rate>
							</div>
						</div>
					</div>

					<!-- <div class="field">
						<div class="control">
							<input class="input" type="text" v-model="title" placeholder="Chủ đề">
						</div>
					</div> -->

					<div class="field">
						<div class="control">
							<textarea class="textarea" v-model="title"
								placeholder="Viết nhận xét của bạn tại đây"></textarea>
						</div>
					</div>

					<div class="field">
						<div class="control">
							<button class="button is-black" @click="submitRatingForm">Submit</button>
						</div>
					</div>
				</div>
			</div>
		</el-col>
	</el-row>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapState, mapGetters, mapMutations } from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';
import { ElMessage } from "element-plus";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';

@Options({
	components: {
		FontAwesomeIcon,
	},

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
		...mapActions("post", [ActionTypes.ADD_POST_BOOKMARK, ActionTypes.LIKE_POST, ActionTypes.RATE_POST]),

		async actionPost(action: String) {
			if (this.userInfo.id) {
				if (action == "save") {
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
				else if (action == "unsave") {
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
				else if (action == "like") {
					let res = await this.LIKE_POST(this.postDetail.id)
					if (res.status == 200) {
						this.postDetail.has_liked = true
						this.postDetail.likes = res.data.likes
					}
				}
				else if (action == "unlike") {
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

		async submitRatingForm() {
			if (this.userInfo.id) {
				let res = await this.RATE_POST({
					id: this.postDetail.id,
					feedback: {
						title: this.title,
						content: this.feedback,
						star_rating: this.rating
					}
				})

				if (res.data.detail == 'you have created rating ') {
					ElMessage('Bạn đã đánh giá bài viết này trước đây!')
					this.ratingSection = false
				}
				else {
					ElMessage({
						message: `Cảm ơn bạn đã đánh giá bài viết này.`,
						type: 'success',
					})
				}
			}
			else {
				this.$router.push("/login")
			}
		},
	},
	created() {
		for (let rate in this.postDetail.post_rating) {
			if (this.postDetail.post_rating[rate].id == this.userInfo.id)
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
}</style>