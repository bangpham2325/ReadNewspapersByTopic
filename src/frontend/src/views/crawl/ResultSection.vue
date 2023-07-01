<template>
	<el-row style="text-align: center;margin-left:6%">
		<el-col :span="span" v-if="selectedSource.includes('Vietnamnet')">
			<el-progress type="dashboard" :percentage="100" color="#5cb87a">
				<el-button type="success" icon="Check" circle />
			</el-progress>
			<p class="subtitle is-6">Vietnamnet</p>
		</el-col>
			
		<el-col :span="span" v-if="selectedSource.includes('Vietcetera')">
			<el-progress type="dashboard" :percentage="100" color="#5cb87a">
				<el-button type="success" icon="Check" circle />
			</el-progress>
			<p class="subtitle is-6">Vietcetera</p>
		</el-col>

		<el-col :span="span" v-if="selectedSource.includes('Dantri')">
			<el-progress type="dashboard" :percentage="100" color="#5cb87a">
				<el-button type="success" icon="Check" circle />
			</el-progress>
			<p class="subtitle is-6">Dantri</p>
		</el-col>

		<el-col :span="span" v-if="selectedSource.includes('Vnexpress')">
			<el-progress type="dashboard" :percentage="100" color="#5cb87a">
				<el-button type="success" icon="Check" circle />
			</el-progress>
			<p class="subtitle is-6">Vnexpress</p>
		</el-col>
	</el-row>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';


@Options({
	props: {
		selectedSource: [],
		data_crawl: [] as any,
	},
	data() {
    return {
			span: 0,
			vietnamnet: {},
			vietcetera: {},
			dantri: {},
			vnexpress: {}
		}
	},
	created(){
		if(this.selectedSource.length == 4)
			this.span = 6
		else if (this.selectedSource.length == 3)
			this.span = 8
		else if (this.selectedSource.length == 2)
			this.span = 12
		else
			this.span = 24
	}

})
export default class ResultSection extends Vue {}
</script>