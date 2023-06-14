<template>
	<h1 class="title" style="  text-align: center; font-size: 40px; margin-bottom: 50px;">Blog Cá Nhân</h1>
	<div class="tile is-ancestor layout-post" v-loading="loading">
		<div v-for="post in blog_posts">
			<div class="tile is-parent" @click="detailPost(post.slug)">
				<div class="tile is-child box card">
					<div class="card-image">
						<figure class="image is-3by2">
							<img :src=post.thumbnail alt="Placeholder image">
						</figure>
					</div>
					<div class="card-content">

						<el-row>
							<el-col :span="20">
								<el-row>
									<p class="title is-6 mt-3" style="color:#00773e;">{{ post.category.title }}</p>
								</el-row>
							</el-col>
							<el-col :span="4">
								<el-row class="is-flex is-justify-content-right">
									<el-button type="text" icon="View" style="color:#00773e;" size="large">{{ post.views
									}}</el-button>
								</el-row>
							</el-col>
						</el-row>

						<p class="title is-5">{{ post.title }}</p>
						<p class="desc">{{ post.summary }}</p>

						<el-row>
							<el-col :span="12">
								<el-button type="text" icon="Histogram" style="color:black;" size="large"
									class="title is-6 mt-1" v-if="post.avg_rating != null">{{ post.avg_rating
									}}</el-button>
								<el-button type="text" icon="Histogram" style="color:black;" size="large"
									class="title is-6 mt-1" v-else>0</el-button>
							</el-col>
							<el-col :span="12">
								<el-row class="is-flex is-justify-content-right">
									<p class="title is-6 mt-4">{{ post.publish_date }}</p>
								</el-row>
							</el-col>
						</el-row>
					</div>
				</div>
			</div>
		</div>
	</div>
	<Pagination :total="total" :page="query.page" :page_size="query.page_size" @changePage="query.page = $event">
	</Pagination>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapMutations } from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';
import Pagination from "@/components/Pagination.vue";
import Posts from '@/types/post/PostItem';

@Options({
	components: {
		Pagination
	},
	data() {
		return {
			blog_posts: [] as Posts[],
			query: {
				page: 1,
				page_size: 12,
				search: "",
				categories: []
			},
			total: 0,
			loading: true,
		}
	},

	methods: {
		...mapMutations(["SET_LOADING"]),
		...mapActions("post", [ActionTypes.FETCH_POST_BLOG]),

		async getBlogPosts() {
			this.loading = true
			this.SET_LOADING(true)
			let data = await this.FETCH_POST_BLOG(this.query)
			this.blog_posts = data.results as Posts[]
			this.total = data.count
			this.SET_LOADING(false)
			this.loading = false
		},
		async handleCurrentChange(currentPage: any) {
			this.currentPage = currentPage;
			await this.getPosts(this.currentPage, this.filterStatus)
			this.scrollToTop()
		},
		detailPost(post_slug: string) {
			this.$router.push({ name: 'detail-post', params: { slug: post_slug } })
		},
	},
	watch: {
		query: {
			deep: true,
			handler: async function () {
				await this.getBlogPosts();
				this.$router.replace({ query: this.query }).catch((err: any) => err);
			},
		}
	},
	computed: {
		component2Class() {
			return 'blog-personal';
		},
	},

	async created() {
		await this.getBlogPosts()
		this.loading = false
	}
})

export default class BlogPostPage extends Vue {
}
</script>

<style scoped>
.carousel-item {
	color: #475669;
	text-align: center;
}

.tile.is-ancestor.layout-post {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	grid-gap: 10px;
	position: relative;
	padding-bottom: 20px;
}

.is-child {
	cursor: pointer;
	transition: all 0.3s ease;
	padding: 0;
	box-shadow: 1px 1px 10px #b3b3b3;
	border-radius: 8px;
	overflow: hidden;
	transform: translate(0, 0);
}

.is-child:hover {
	box-shadow: 1px 3px 20px #898989;
	transform: translate(2px, -2px);

}

.card-content {
	padding-top: 0;
	padding-bottom: 0;
}

.title {
	height: 45px;
	max-height: 45px;
	overflow: hidden;
	display: -webkit-box;
	-webkit-box-orient: vertical;
	-webkit-line-clamp: 2;
	margin-bottom: 15px;
}

.desc {
	font-size: 0.9rem;
	height: 45px;
	max-height: 45px;
	overflow: hidden;
	display: -webkit-box;
	-webkit-box-orient: vertical;
	-webkit-line-clamp: 2;
	margin-bottom: 15px;
}

.title.is-6.mt-3 {
	height: 20px;
}

.el-button {
	display: flex;
	align-items: center;
	padding-left: 0;
}

/* h2 {
  margin-top: 0;
  font-size: 24px;
  color: #333;
}

p {
  margin-bottom: 10px;
  color: #666;
}

strong {
  font-weight: bold;
}

.date {
  font-style: italic;
}
*/
</style>