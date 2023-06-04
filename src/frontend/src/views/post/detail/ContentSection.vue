<template>
	<div v-for="content in contents">
		<h2 class="title is-3">{{ content.title }}</h2>

		<div v-for="line in content.paragraph">
			<p class="my-5">{{ line.text }}</p>
			<div v-if="line.below_img">
				<figure class="image is-2by1 my-6">
					<img :src=content.image>
				</figure>
				<p class="subtitle is-6 is-flex is-justify-content-center has-text-centered"><b><i>{{ content.description_img }}</i></b></p>
			</div>
			
		</div>
	</div>

</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';

@Options({
	props: {
    contents: [] as any,
  },
})

export default class ContentSection extends Vue {
}
</script>

<style>

</style>