<template>
	<div v-for="content in contents">
		<h2 class="title is-3">{{ content.title }}</h2>

		<div v-for="line in content.paragraph">
			<p>{{ line.text }}</p>
			<figure class="image is-2by1 my-6" v-if="line.above_img">
				<img :src=content.image>
			</figure>
		</div>
	</div>

	<el-tag class="mr-4" size="large" v-for="i in 5">Tag 1</el-tag>

</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';

@Options({
	props: {
    contents: [] as any
  },
})

export default class ContentSection extends Vue {
}
</script>

<style>

</style>