<template>
	<h2 class="title is-3">Tin tức mới nhất</h2>
	<div class="tile is-ancestor layout-post">
		<template v-for="post in new_posts">
			<div :class="['tile', 'is-parent']" @click="detailPost(post.id)">
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
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapMutations } from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';
import { ElMessage } from "element-plus";

@Options({
	data() {
		return {
			new_posts: [] as any,
		}
	},

	methods: {
		...mapMutations(["SET_LOADING"]),
		...mapActions("post", [ActionTypes.FETCH_POST_NEW]),

		async getNewPosts() {
			this.SET_LOADING(true)
			let data = await this.FETCH_POST_NEW()
			if (data) {
				this.new_posts = data
			}
			this.SET_LOADING(false)
		},

		detailPost(post_id: string) {
			this.$router.push({ name: 'detail-post', params: { id: post_id } })
		},
	},

	async created() {
		await this.getNewPosts()
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