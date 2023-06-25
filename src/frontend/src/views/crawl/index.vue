<template>
	<h1 class="title is-3 my-5" style="margin-left:7%;">Thu thập bài báo</h1>
  <el-steps :active="step" align-center finish-status="success" class="mr-6">
    <el-step title="Chọn nguồn" description="Lựa chọn trang website" />
    <el-step title="Thu thập" description="Lấy thông tin từ các nguồn" />
    <el-step title="Kết quả" description="Các bài viết đã thu thập được" />
  </el-steps>

	<div class="mx-6 px-6 mt-6">
		<div v-if="step==0" class="space">
			<SourceSection @source-selected="handleSource"></SourceSection>
		</div>

		<div v-if="step==1" class="space my-5">
			<CrawlSection :selectedSource="source" @status="hanldeProcess" @data-crawl="handleDataCrawl"></CrawlSection>
		</div>

		<div v-if="step==2" class="space">
			<ResultSection :selectedSource="source" :data="data"></ResultSection>
		</div>
	
		<div v-if="step < 2" class="is-flex is-justify-content-center">
			<button :disabled="source.length==0 || status" class="button is-success is-rounded" @click="confirmSource=true">Tiếp theo</button>
		</div>
	
		<div v-else class="is-flex is-justify-content-center">
			<button class="button is-success is-rounded" @click="goDashboard">Hoàn thành</button>
		</div>
		<el-dialog v-model="confirmSource" title="Xác nhận" width="30%" center>
			<span>
				Bạn đã chọn các trang <span v-for="name in source" :key="name">{{ name }}-</span> này. Bắt đầu thu thập bài viết sau khi bạn chọn thu nhập.
			</span>
			<template #footer>
				<span class="dialog-footer">
					<el-button @click="confirmSource = false">Hủy</el-button>
					<el-button type="primary" @click="crawl">
						Thu thập
					</el-button>
				</span>
			</template>
		</el-dialog>
	</div>

</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import SourceSection from './SourceSection.vue';
import CrawlSection from './CrawlSection.vue';
import ResultSection from './ResultSection.vue';

@Options({
	components: {
		SourceSection,
		CrawlSection,
		ResultSection,
	},
	data() {
    return {
			step: 0,
			source: [],
			confirmSource: false,
			status: false,
			data: [] as any
		}
	},

	methods: {
		hanldeProcess(data: boolean){
			this.status = data
		},
		handleSource(data: []){
			this.source = data
		},
		handleDataCrawl(data: any){
			this.data = data
		},
		crawl(){
			this.step = this.step + 1
			if(this.confirmSource)
				this.confirmSource = !this.confirmSource
		},
		goDashboard(){
			this.$router.push("/post/management")
		}
	}
})
export default class CrawlPage extends Vue {}
</script>

<style lang="scss" scoped>
.space {
	margin-right: 6%;
}
</style>