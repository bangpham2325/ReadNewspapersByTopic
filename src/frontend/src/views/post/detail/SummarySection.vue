<template>
	<el-tooltip :content=postDetail.publish_date placement="top-start">
		<p class="title is-6" style="color:#808080">{{ postDetail.publish_date }}</p>
	</el-tooltip>

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
				<el-button type="text" icon="CollectionTag" style="color:#00773e;" size="large" @click="actionPost('save')">BOOKMARK</el-button>
				<el-button type="text" icon="View" style="color:#00773e;" size="large">{{ postDetail.views }}</el-button>
				<el-tooltip content="Like" placement="top-start">
					<el-button type="text" icon="Star" style="color:#00773e;" size="large" @click="actionPost('like')">{{ postDetail.likes }}</el-button>
				</el-tooltip>
				<el-button type="text" icon="ChatRound" style="color:#00773e;" size="large" @click="ratingSection=true">{{ postDetail.total_rating }}</el-button>
			</el-row>
		</el-col>

		<el-dialog v-model="ratingSection" title="Shipping address">
			<el-table :data="gridData">
				<el-table-column property="date" label="Date" width="150" />
				<el-table-column property="name" label="Name" width="200" />
				<el-table-column property="address" label="Address" />
			</el-table>
		</el-dialog>
	</el-row>

</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapState, mapGetters, mapMutations} from "vuex";

@Options({
	props: {
		postDetail: {},
	},

	methods: {
		actionPost(action: String){
			if(this.userInfo){
				if(action == "save"){
					console.log("abc")
				}
				else if(action == "like"){
					console.log("123")
				}
			}
			else {
				this.$router.push("/login")
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