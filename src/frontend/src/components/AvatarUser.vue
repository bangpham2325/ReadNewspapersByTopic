<template>
<div class="top-bar">
	<el-row class="p-3" justify="space-between">
			<div class="top-bar__right-menu columns is-vcentered is-flex is-justify-content-end">
				<div class="top-bar__right-menu__avatar">
					<div class="dropdown is-hoverable">
						<div class="dropdown-trigger">
							<figure class="image">
								<img v-if="avatar" class="is-rounded" :src="avatar" alt="Avatar">
								<img v-else class="is-rounded" src="@/assets/vectors/default_avatar.svg" alt="Avatar">
							</figure>
						</div>
						<div class="dropdown-menu" id="dropdown-menu" role="menu">
							<div class="dropdown-content">
								<router-link to="/post/management" class="dropdown-item ml-3" v-if="this.userInfo.role == 'ADMIN'">
									Dashboard
								</router-link>
								<router-link to="/post/my-posts" class="dropdown-item ml-2" v-if="this.userInfo.role == 'AUTHOR'">
								    My Posts
								</router-link>
								<router-link to="/profile/edit" class="dropdown-item">
									Profile
								</router-link>
								<router-link to="/post/saved" class="dropdown-item">
									Saved
								</router-link>
								<hr class="dropdown-divider">
								<router-link to="/logout" class="dropdown-item">
									Log Out
								</router-link>
							</div>
						</div>
					</div>
				</div>
			</div>
	</el-row>
</div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import 'element-plus/theme-chalk/display.css';
import {mapState, mapGetters} from "vuex";

@Options({
	props: {
		avatar: ""
	},
	computed: {
    ...mapState(["is_loading"]),
    ...mapGetters("user", ["userInfo"]),
  },
})

export default class TopBar extends Vue {
avatar!: string
}
</script>

<style scoped lang="scss">
figure, p {
margin: 0;
}

.top-bar {

&__greeting {
	min-width: 250px;
	display: inline-block;

	&__name {
		display: block;
		font-weight: 400;
		text-transform: capitalize;
	}

	&__text {
		display: block;
		font-size: 1rem;
	}
}

&__search-bar {
	.control {
		.input, .icon {
			transition: all 0.3s ease-in-out;
		}
	}
}

&__right-menu {
	&__avatar {
		img {
			height: 52px;
			width: 52px;
			cursor: pointer;
		}
	}

	&__notification {
		cursor: pointer;
		font-size: 1.6rem;
		color: #ccc;

		:hover {
			color: #024547;
			transition: color 0.2s ease-in-out;
		}
	}

	#dropdown-menu {
		font-weight: 400;
		position: absolute;
		top: 50px;
		left: -130px;
		z-index: 1;
	}
}
}
</style>