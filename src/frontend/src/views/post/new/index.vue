<template>
	<div v-loading="loading">
		<h2 class="title is-3">Tin tức mới nhất</h2>
		<div class="tile is-ancestor layout-post">
			<template v-for="post in new_posts">
				<div :class="['tile', 'is-parent']" @click="detailPost(post.slug)">
					<div :class="['tile', 'is-child', 'box card']">
						<div class="card-image">
							<figure class="image is-3by2">
								<img :src=post.thumbnail alt="Placeholder image">
							</figure>
						</div>
						<div class="card-content">
							<el-row class="mb-3">
								<el-row class="is-flex is-justify-content-right">
									<p class="title is-6" style="color:#00773e;">{{ post.category.title }}</p>
								</el-row>
							</el-row>

							<p class="title is-5" style="min-height:70px;">{{ post.title }}</p>
							<p style="color:#808080; font-size: 12px; min-height:100px;">{{ post.summary }}</p>

							<el-row>
								<el-col :span="14">
									<el-row>
										<el-avatar :size="40" class="mt-1">
											<img
												src="https://img.vietcetera.com/uploads/avatar-images/12-apr-2023/vu-hoang-long-1681282620604-160x160.jpg">
										</el-avatar>
										<p class="title is-6 mt-4 ml-4" style="color:#00773e;">{{ post.author }}</p>
									</el-row>
								</el-col>

								<el-col :span="10">
									<el-row class="is-flex is-justify-content-right">
										<p class="title is-6 mt-4">{{ post.publish_date }}</p>
									</el-row>
								</el-col>
							</el-row>
						</div>
					</div>
				</div>
			</template>
		</div>
		<Pagination :total="total" :page="query.page" :page_size="query.page_size" @changePage="query.page = $event">
		</Pagination>
	</div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapMutations, mapGetters, mapState } from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';
import { ElMessage } from "element-plus";
import Posts from '@/types/post/PostItem';
import Pagination from "@/components/Pagination.vue";

@Options({
	components: {
		Pagination
	},
	data() {
		return {
			new_posts: [] as Posts[],
			totalPage: 10,
			loading: true,
			categories: [],
			query: {
				page: 1,
				page_size: 12,
				search: "",
				categories: []
			},
			total: 0,
		}
	},

	methods: {
		...mapMutations(["SET_LOADING"]),
		...mapActions("post", [ActionTypes.FETCH_POST_NEW]),

		async getNewPosts(page: any = null) {
			this.SET_LOADING(true)
			let data: any
			data = await this.FETCH_POST_NEW(this.query)
			this.new_posts = data.results as Posts[]
			this.total = data.count as 0
			this.SET_LOADING(false)
		},

		detailPost(post_slug: string) {
			this.$router.push({ name: 'detail-post', params: { slug: post_slug } })
		},

		async handleCurrentChange(currentPage: any) {
			this.currentPage = currentPage;
			await this.getNewPosts(this.currentPage)
			this.scrollToTop()
		},

		scrollToTop() {
			window.scrollTo({
				top: 0,
				behavior: 'smooth',
			});
		},

	},
	watch: {
		query: {
			deep: true,
			handler: async function () {
				await this.getNewPosts();
				this.$router.replace({ query: this.query }).catch((err: any) => err);
			},
		}
	},
	computed: {
		...mapState(["is_loading"]),
		...mapGetters("user", ["userInfo"]),
	},

	async created() {
		await this.getNewPosts()
		this.loading = false
	}
})

export default class NewPostPage extends Vue {
}
</script>

<style scoped>
.carousel-item {
	color: #475669;
	text-align: center;
}

.tile.is-ancestor.layout-post {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	grid-gap: 10px;
}
</style>