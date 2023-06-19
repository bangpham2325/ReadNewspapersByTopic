<template>
	<el-row>
		<el-col :span="12">
			<h1 class="title is-2">Kết quả</h1>
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

	<div class="card mb-6" v-for="post in posts" v-loading="loading">
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
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapState, mapGetters, mapMutations } from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';

@Options({
	data() {
		return {
			posts: {} as any,
			time: '',
			loading: true,
			start_date: '',
			end_date: '',
		}
	},

	methods: {
		...mapMutations(["SET_LOADING"]),
		...mapActions("post", [ActionTypes.FETCH_POST_BY_FILTER]),

		async getPostByFilter() {
			this.time = ''
			this.loading = true
			const query = {
				search: this.$route.params.text
			}
			let data = await this.FETCH_POST_BY_FILTER(query)
			if (data) {
				this.posts = data.results
			}
			this.loading = false
		},

		detailPost(post_slug: string) {
			this.$router.push({ name: 'detail-post', params: { slug: post_slug } })
		},

		async filterByDate(){
			this.loading = true
			this.start_date = this.time[0].toLocaleDateString('en-CA')
			this.end_date = this.time[1].toLocaleDateString('en-CA')
			let data = await this.FETCH_POST_BY_FILTER({
				search: this.$route.params.text,
				start_date: this.start_date,
				end_date: this.end_date
			})
			if (data) {
				this.posts = data.results
				this.loading = false
			}
		}
	},

	watch: {
		async $route() {
			await this.getPostByFilter()
		}
	},

	async created() {
		await this.getPostByFilter()
		this.loading = false
	}

})

export default class SearchPage extends Vue {
}
</script>

<style></style>