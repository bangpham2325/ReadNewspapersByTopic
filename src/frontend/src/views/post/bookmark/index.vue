<template>
	<div v-loading="loading">
		<h1 class="title is-2">Đã lưu</h1>

		<div class="card mb-6" v-for="post in posts">
			<el-row @click="detailPost(post.slug)">
				<el-col :span="6">
					<figure class="image is-3by2" style="height:100%;">
						<img :src=post.thumbnail alt="Placeholder image">
					</figure>
				</el-col>

				<el-col :span="18">
					<div class="card-content">
						<p class="title is-5" style="color:#00773e">{{ post.category.title }}</p>
						<h2 class="title is-3">{{ post.title }}</h2>
						<p class="subtitle is-5 mt-1" style="color:#808080">{{ post.summary }}</p>

						<el-row>
							<el-avatar :size="60">
								<img
									src="https://img.vietcetera.com/uploads/avatar-images/12-apr-2023/vu-hoang-long-1681282620604-160x160.jpg" />
							</el-avatar>
							<p class="title is-5 mt-4 ml-4">{{ post.author }} - {{ post.publish_date }}</p>
						</el-row>
					</div>
				</el-col>
			</el-row>
		</div>
	</div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapState, mapGetters, mapMutations } from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';

@Options({
	data() {
		return {
			posts: {} as any,
			loading: true,
		}
	},

	methods: {
		...mapMutations(["SET_LOADING"]),
		...mapActions("post", [ActionTypes.FETCH_POST_BY_BOOKMARK]),

		async getPostByBookmark() {
			this.SET_LOADING(true)
			let data = await this.FETCH_POST_BY_BOOKMARK()
			if (data) {
				this.posts = data
			}
			this.SET_LOADING(false)
		},

		detailPost(post_slug: string) {
			this.$router.push({ name: 'detail-post', params: { slug: post_slug } })
		}
	},

	async created() {
		await this.getPostByBookmark()
		this.loading = false
	}

})

export default class BookmarkPage extends Vue {
}
</script>

<style></style>