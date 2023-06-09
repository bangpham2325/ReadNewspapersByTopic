<template>
	<el-row v-if="postDetail.status=='PUBLISHED'" class="is-flex is-justify-content-right mb-6">
		<button v-if="this.userInfo.role === 'ADMIN'" class="button is-dark" @click="statusPost('DRAFT')">Ẩn bài viết</button>
		<button v-if="this.userInfo.role === 'ADMIN'" class="button is-danger ml-2" @click="deletePost">Xóa bài viết</button>
	</el-row>

	<el-row v-else class="is-flex is-justify-content-right mb-6">
		<button class="button is-primary" style="background-color: #00773e;" @click="statusPost('PUBLISHED')">Đăng bài viết</button>
		<button class="button is-danger ml-2" @click="deletePost">Xóa bài viết</button>
	</el-row>

	<el-row>
		<el-col :span="12">
			<el-tooltip :content=postDetail.publish_date placement="top-start">
				<p class="title is-6" style="color:#808080">{{ postDetail.publish_date }}</p>
			</el-tooltip>
		</el-col>
		<el-col :span="12">
			<el-row class="is-flex is-justify-content-right" v-if="this.userInfo.role== 'ADMIN'">
				<el-tag v-if="postDetail.status=='DRAFT'" type="info" effect="dark" size="large">{{ postDetail.status }}</el-tag>
				<el-tag v-else type="success" effect="dark" size="large">{{ postDetail.status }}</el-tag>
			</el-row>
		</el-col>
	</el-row>
	

	<p class="title is-5" style="color:#00773e">{{ postDetail.category.title }}</p>
	<h1 class="title is-2">{{ postDetail?.title }}</h1>
	<p class="subtitle is-5" style="color:#808080">{{ postDetail.summary }}</p>
	
	<el-row>
		<el-col :span="12">
			<el-row>
					<el-avatar :size="50">
						<img src="https://img.vietcetera.com/uploads/avatar-images/12-apr-2023/vu-hoang-long-1681282620604-160x160.jpg">
					</el-avatar>
					<p class="title is-6 mt-4 ml-4" style="color:#00773e;">{{ postDetail.author }}</p>
			</el-row>
		</el-col>

		<el-col :span="12">
			<el-row class="is-flex is-justify-content-right">
				<el-button type="text" icon="Connection" style="color:#00773e;font-size: 17px;" size="large" @click="openSource">Nguồn</el-button>
				<el-button type="text" icon="View" style="color:#00773e;" size="large">{{ postDetail.views }}</el-button>
				<el-button type="text" icon="ChatLineRound" style="color:#00773e;" size="large">{{ postDetail.total_comment }}</el-button>
			</el-row>
		</el-col>
	</el-row>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapState, mapGetters, mapMutations} from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';
import {ElMessage} from "element-plus";

@Options({
	props: {
		postDetail: {},
	},

	methods: {
		...mapMutations(["SET_LOADING"]),
    ...mapActions("post", [ActionTypes.UPDATE_STATUS_POST, ActionTypes.DELETE_POST]),

		openSource(){
			window.open(this.postDetail.source.domain, '_blank');
		},

		async statusPost(status:string){
			let res = await this.UPDATE_STATUS_POST({id: this.postDetail.id, status: {status: status}})
			if (res.status == 200){
				window.location.reload();
				if(status == 'PUBLISHED')
					ElMessage({
						message: `Đăng bài ${this.postDetail.title} thành công.`,
						type: 'success',
					})
				else {
					ElMessage({
						message: `Ẩn bài ${this.postDetail.title} thành công.`,
						type: 'success',
					})
				}
			}
			else{
				ElMessage.error('Đã có lỗi xảy ra.')
			}
		},

		async deletePost(){
			let res = await this.DELETE_POST(this.postDetail.id)
			if(res.status == 204){
				ElMessage({
						message: `Xóa bài viết thành công.`,
						type: 'success',
					})
				this.$router.push('/post/management')
			}
			else{
				ElMessage.error('Đã có lỗi xảy ra.')
			}
		}

	},
	computed: {
    ...mapState(["is_loading"]),
    ...mapGetters("user", ["userInfo"]),
  },
})

export default class SummarySection extends Vue {
}
</script>

<style>

</style>