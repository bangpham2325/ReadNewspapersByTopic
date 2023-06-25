<template>
	<el-row style="text-align: center;">
		<el-col :span="span" v-if="selectedSource.includes('Vietnamnet')">
			<el-progress type="dashboard" :percentage="100" color="#5cb87a">
				<el-button type="success" icon="Check" circle />
			</el-progress>
			<p class="subtitle is-6">Vietnamnet</p>
			<p class="subtitle is-6">{{ data.vietnamnet.data }}</p>
		</el-col>
			
		<el-col :span="span" v-if="selectedSource.includes('Vietcetera')">
			<el-progress type="dashboard" :percentage="100" color="#5cb87a">
				<el-button type="success" icon="Check" circle />
			</el-progress>
			<p class="subtitle is-6">Vietcetera</p>
			<p class="subtitle is-6">{{ data.vietcetera.data }}</p>
		</el-col>

		<el-col :span="span" v-if="selectedSource.includes('Dantri')">
			<el-progress type="dashboard" :percentage="100" color="#5cb87a">
				<el-button type="success" icon="Check" circle />
			</el-progress>
			<p class="subtitle is-6">Dantri</p>
			<p class="subtitle is-6">{{ data.dantri.data }}</p>
		</el-col>

		<el-col :span="span" v-if="selectedSource.includes('Vnexpress')">
			<el-progress type="dashboard" :percentage="100" color="#5cb87a">
				<el-button type="success" icon="Check" circle />
			</el-progress>
			<p class="subtitle is-6">Vnexpress</p>
			<p class="subtitle is-6">{{ data.vnexpress.data }}</p>
		</el-col>
	</el-row>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';


@Options({
	props: {
		selectedSource: [],
		data: [] as any
	},
	data() {
    return {
			span: 0,
		}
	}

})
export default class ResultSection extends Vue {}
</script>