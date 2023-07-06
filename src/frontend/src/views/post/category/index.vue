<template :key="$route.params.name">
	<el-row>
		<el-col :span="12">
			<h1 class="title is-3 mt-3">{{ titleCategory }}</h1>
		</el-col>

		<el-col :span="12" class="is-flex is-justify-content-right">
			<div class="block mt-2">
				<el-date-picker
				v-model="time"
				type="daterange"
				start-placeholder="Ngày"
				end-placeholder="Ngày"
				@change="filterByDate"
				/>
			</div>
		</el-col>
	</el-row>
	<div class="mt-5" v-loading="loading">
		<div class="card mb-6" v-for="post in postCategory">
			<el-row @click="detailPost(post.slug)">
				<el-col :span="6">
					<figure class="image is-3by2" style="height:auto;">
						<img :src=post.thumbnail alt="Placeholder image">
					</figure>
				</el-col>

				<el-col :span="18">
					<div class="card-content">
						<p class="title is-5" style="color:#00773e">{{ titleCategory }}</p>
						<h2 class="title is-4 mb-3">{{ post.title }}</h2>
						<p class="subtitle is-6 mt-1" style="color:#808080">{{ post.summary }}</p>

						<el-row>
							<el-avatar :size="45">
								<img
									src="https://img.vietcetera.com/uploads/avatar-images/12-apr-2023/vu-hoang-long-1681282620604-160x160.jpg" />
							</el-avatar>
							<p class="title is-6 mt-4 ml-4">{{ post.author }} - {{ post.publish_date }}</p>
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
import Pagination from "@/components/Pagination.vue";

@Options({
	components: {
		Pagination
	},
	data() {
		return {
			postCategory: {} as any,
			titleCategory: this.$route.params.name,
			time: '',
			loading: true,
			start_date: '',
			end_date: '',
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
		},

		async filterByDate(){
			this.loading = true
			this.start_date = this.time[0].toLocaleDateString('en-CA')
			this.end_date = this.time[1].toLocaleDateString('en-CA')
			let data = await this.FETCH_POST_BY_FILTER({
				page: 1,
				page_size: 12,
				search: "",
				categories: "",
				start_date: this.start_date,
				end_date: this.end_date
			})
			if (data) {
				this.postCategory = data.results
				this.total = data.count as 0
				this.loading = false
			}
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