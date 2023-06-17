<template :key="$route.params.name">
	<div v-loading="loading">
		<h1 class="title is-2">{{ titleCategory }}</h1>
		<div class="card mb-6" v-for="post in postCategory">
			<el-row @click="detailPost(post.slug)">
				<el-col :span="6">
					<figure class="image is-3by2" style="height:100%;">
						<img :src=post.thumbnail alt="Placeholder image">
					</figure>
				</el-col>

				<el-col :span="18">
					<div class="card-content">
						<p class="title is-5" style="color:#00773e">{{ titleCategory }}</p>
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
		<Pagination :total="total" :page="query.page" :page_size="query.page_size" @changePage="query.page = $event">
		</Pagination>
	</div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapMutations } from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';
import { RouteLocationNormalized } from 'vue-router';
import Pagination from "@/components/Pagination.vue";

@Options({
	components: {
		Pagination
	},
	data() {
		return {
			postCategory: {} as any,
			titleCategory: this.$route.params.name,
			loading: true,
			total: 0,
			totalPage: 10,
			query: {
				page: 1,
				page_size: 12,
				search: "",
				categories: ""
			},
		}
	},

	methods: {
		...mapMutations(["SET_LOADING"]),
		...mapActions("post", [ActionTypes.FETCH_POST_BY_FILTER]),

		async getPostByCategory() {
			this.SET_LOADING(true)
			let data = await this.FETCH_POST_BY_FILTER(this.query)
			if (data) {
				this.postCategory = data.results
				this.total = data.count as 0
			}
			this.SET_LOADING(false)
		},

		detailPost(post_slug: string) {
			this.$router.push({ name: 'detail-post', params: { slug: post_slug } })
		}
	},

	watch: {
		query: {
			deep: true,
			handler: async function () {
				this.$router.replace({ query: this.query }).catch((err: any) => err);
				await this.getPostByCategory();
			},
		}
	},

	async created() {
		this.query.categories = this.$route.query.id
		await this.getPostByCategory()
		this.loading = false
	}

})

export default class PostCategoryPage extends Vue {
}
</script>

<style></style>