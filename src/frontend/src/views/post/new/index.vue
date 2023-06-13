<template>
	<div v-loading="loading">
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

            <p class="title is-5" style="min-height:70px;">{{  post.title }}</p>
            <p style="color:#808080; font-size: 12px; min-height:100px;">{{ post.summary }}</p>

						<el-row>
							<el-col :span="14">
								<el-row>
										<el-avatar :size="40" class="mt-1">
											<img src="https://img.vietcetera.com/uploads/avatar-images/12-apr-2023/vu-hoang-long-1681282620604-160x160.jpg">
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
	<div class="is-flex is-justify-content-center mt-4">
		<el-pagination 
			background 
			layout="prev, pager, next" 
			:total=totalPage
			@current-change="handleCurrentChange"/>
	</div>
	</div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapMutations, mapGetters, mapState} from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';
import {ElMessage} from "element-plus";

@Options({
	data(){
		return {
			new_posts: [] as any,
			totalPage: 10,
			loading: true, 
			categories: [],
		}
	},

	methods: {
		...mapMutations(["SET_LOADING"]),
		...mapActions("post", [ActionTypes.FETCH_POST_NEW]),

		async getNewPosts(page:any = null){
      this.SET_LOADING(true)
			let data: any
			for (const element of this.userInfo.categories) {
				if(!this.categories.includes(element.id))
					this.categories.push(element.id)
			}
			if(page){
				data = await this.FETCH_POST_NEW({categories: this.categories, page: page})
			}
			else
				data = await this.FETCH_POST_NEW({categories: this.categories})
			if (data){
				this.totalPage = Math.ceil(data.count/12)*10
				this.new_posts = data.results
			}
			this.SET_LOADING(false)
		},

		detailPost(post_id: string){
      this.$router.push({ name: 'detail-post', params: { id: post_id } })
    },

		async handleCurrentChange(currentPage:any) {
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

	computed: {
    ...mapState(["is_loading"]),
    ...mapGetters("user", ["userInfo"]),
  },

	async created(){
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

.tile.is-ancestor.layout-post{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 10px;
}
</style>