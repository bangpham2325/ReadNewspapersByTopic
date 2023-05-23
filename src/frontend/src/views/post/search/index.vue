<template>
	<h1 class="title is-2">Kết quả</h1>

  <div class="card mb-6" v-for="post in posts">
		<el-row @click="detailPost(post.id)">
			<el-col :span="6">
					<figure class="image is-3by2" style="height:100%;">
						<img :src=post.thumbnail alt="Placeholder image">
					</figure>
			</el-col>

			<el-col :span="18">
				<div class="card-content">
					<p class="title is-5" style="color:#00773e">{{ titleCategory }}</p>
					<h2 class="title is-3">{{ post.title }}</h2>
					<p class="subtitle is-5 mt-1" style="color:#808080">{{post.summary}}</p>
					
					<el-row>
						<el-avatar :size="60">
							<img src="https://img.vietcetera.com/uploads/avatar-images/12-apr-2023/vu-hoang-long-1681282620604-160x160.jpg"/>
						</el-avatar>
						<p class="title is-5 mt-4 ml-4">{{post.author}} - {{post.publish_date}}</p>
					</el-row>
				</div>
			</el-col>
		</el-row>	
	</div>

</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapState, mapGetters, mapMutations} from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';

@Options({
	data(){
		return {
			posts: {} as any,
		}
	},

	methods: {
		...mapMutations(["SET_LOADING"]),
    ...mapActions("post", [ActionTypes.FETCH_POST_BY_FILTER]),

		async getPostByFilter(){
			this.SET_LOADING(true)
			const query = {
				categories: this.$route.params.text,
				title: this.$route.params.text,
				author: this.$route.params.text
			}
			console.log(query)
			let data = await this.FETCH_POST_BY_FILTER(query)
			if(data) {
				this.posts = data.results
			}
			console.log(this.posts)
			this.SET_LOADING(false)
		},

		detailPost(post_id: string){
      this.$router.push({ name: 'detail-post', params: { id: post_id } })
    }
	},

	// watch: {
  //   async $route(){
	// 		await this.getPostByFilter()
	// 		this.titleCategory = this.$route.params.name
	// 		console.log(this.posts)
	// 	}
	// },

	async created(){
		await this.getPostByFilter()
	}

})

export default class SearchPage extends Vue {
}
</script>

<style>

</style>