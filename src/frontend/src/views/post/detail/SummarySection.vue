<template>
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
import {mapState, mapGetters} from "vuex";

@Options({
	props: {
		postDetail: {},
	},

	methods: {
		openSource(){
			window.open(this.postDetail.source.domain, '_blank');
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