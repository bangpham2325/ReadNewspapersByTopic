<template>
	<router-link to="/home">
		<div class="logo is-flex is-justify-content-left">
		  <div class="logo__icon">N</div>
		  <div class="logo__text">Portal</div>
		</div>
	</router-link>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';

@Options({})

export default class LogoWeb extends Vue {
}
</script>

<style lang="scss">
.logo {
	font-size: 1.5rem;
	font-weight: 500;
	text-align: center;

	&__icon {
		display: inline-block;
		height: 40px;
		width: 40px;
		background-color: #121221;
		border-radius: 10px;
		color: white;
	}

	&__text {
		display: inline-block;
		color: #121221;
		text-transform: capitalize;
		transition: visibility 0.1s, opacity 0.3s linear;
		margin-left: 10px;
		opacity: 1;
		overflow: hidden;
	}
}
</style>