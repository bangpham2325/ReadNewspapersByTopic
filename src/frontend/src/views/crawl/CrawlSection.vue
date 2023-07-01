<template>
	<div v-if="process && temp!=3" style="text-align: center;margin-left:6%">
		<el-progress type="dashboard" :percentage="percentage" :color="colors" />
		<p class="title is-6">Đang thu thập dữ liệu!</p>
	</div>
  <div v-if="!process && temp != 3" style="text-align: center;margin-left:6%">
		<el-progress type="dashboard" :percentage="100" color="#5cb87a">
			<el-button type="success" icon="Check" circle />
		</el-progress>
		<p class="title is-6">Đã thu thập xong!</p>
	</div>

	<div v-if="temp == 3" style="text-align: center;">
		<el-progress type="dashboard" :percentage="100" status="exception"></el-progress>
		<p class="title is-6">Đã có lỗi xảy ra. Vui lòng thử lại sau!</p>
	</div>	

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
			data: [],
		}
	},

	methods: {
		async crawlData() {
			const urls: string[] = []
			if(this.selectedSource.includes('Vietnamnet'))
				urls.push(`https://239e-167-71-199-248.ngrok-free.app/api/v1/newspaper/post/crawl_vietnamnet/`)
			if(this.selectedSource.includes('Vietcetera'))
				urls.push(`https://239e-167-71-199-248.ngrok-free.app/api/v1/newspaper/post/crawl_vietcetera/`)
			if(this.selectedSource.includes('Dantri'))
				urls.push(`https://239e-167-71-199-248.ngrok-free.app/api/v1/newspaper/post/crawl_dantri/`)
			if(this.selectedSource.includes('Vnexpress'))	
				urls.push(`https://239e-167-71-199-248.ngrok-free.app/api/v1/newspaper/post/crawl_vnexpress/`)

			
			while(this.process){
				for (const url of urls) {
					await axios.get(url).then(res => {
						if(res){
							this.data.push(res.data.data)
						}
					}).catch(err => {
						this.temp++
					});
				}

				if(this.data.length != 0){
					this.process = false
					this.$emit('data-crawl', this.data);
					this.$emit('status', this.process);
				}

				if(!this.process || this.temp == 3) break;
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
		this.$emit('status', this.process);
	},
})
export default class CrawlSection extends Vue {}
</script>