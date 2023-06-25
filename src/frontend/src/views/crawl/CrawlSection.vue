<template>
	<div v-if="process" style="margin-left:6%">
		<el-progress class="is-flex is-justify-content-center" type="dashboard" :percentage="percentage" :color="colors" />
		<p class="title is-5 is-flex is-justify-content-center">Đang thu thập dữ liệu!</p>
	</div>
  <el-row v-if="!process && temp < 5" style="text-align: center;">
		<el-progress type="dashboard" :percentage="100" color="#5cb87a">
			<el-button type="success" icon="Check" circle />
		</el-progress>
		<p class="subtitle is-6">Đã thu thập xong!</p>
	</el-row>

	<el-row v-if="temp == 5" style="text-align: center;">
		<el-progress type="dashboard" :percentage="100" status="exception"></el-progress>
		<p class="subtitle is-6">Đã có lỗi xảy ra. Vui lòng thử lại sau!</p>
	</el-row>	

</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import axios from 'axios';

@Options({
	props: {
		selectedSource: [],
	},

	data() {
    return {
			temp: 0,
			percentage: 0,
			process: true,
			colors: [
				{ color: '#f56c6c', percentage: 20 },
				{ color: '#e6a23c', percentage: 40 },
				{ color: '#5cb87a', percentage: 60 },
				{ color: '#1989fa', percentage: 80 },
				{ color: '#6f7ad3', percentage: 100 },
			],
		}
	},

	methods: {
		async crawlData() {
			let vnexpress = false
			let vietnamnet = false
			let dantri = false
			let vietcetera = false
			if(this.selectedSource.includes('Vietnamnet'))
				vnexpress = true
			if(this.selectedSource.includes('Vietcetera'))
				vietnamnet = true
			if(this.selectedSource.includes('Dantri'))
				dantri = true
			if(this.selectedSource.includes('Vnexpress'))	
				vietcetera = true

			const params = {
				vnexpress: vnexpress,
				vietnamnet: vietnamnet,
				dantri: dantri,
				vietcetera: vietcetera
			}

			const url = `https://1c15-143-198-221-48.ngrok-free.app/api/v1/newspaper/post/crawl_data/`;
			while(this.process || this.temp < 5){
				await axios.get(url,{params}).then(res => {
					if(res){
						this.process = !this.process
						this.$emit('data-crawl', res.data);
					}
				}).catch(err => {
					this.temp++
				});
			}
		},
	},

	mounted() {
		setInterval(() => {
      this.percentage = (this.percentage % 100) + 10;
    }, 500);
	},

	created() {
		this.crawlData();
		if(this.selectedSource.length == 4)
			this.span = 6
		else if (this.selectedSource.length == 3)
			this.span = 8
		else if (this.selectedSource.length == 2)
			this.span = 12
		else
			this.span = 24

		this.$emit('status', this.process);
	},
})
export default class CrawlSection extends Vue {}
</script>