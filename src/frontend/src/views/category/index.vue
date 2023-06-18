<template>
	<div class="detail-post">
		<h2 class="title is-3">Chọn thể loại của bạn</h2>
		<p class="subtitle is-5">Dựa trên sự lựa chọn của bạn, chúng tôi sẽ hiển thị cho bạn các chủ đề liên quan.</p>

		<div class="buttons">
			<button
				v-for="category in categories"
				:key="category.id"
				:class="['button', 'is-rounded', { 'is-dark': selectedList.includes(category.id) }]"
				@click="toggleCategory(category.id)"
			>
				{{ category.title }}
			</button>
		</div>

    <div class="is-flex is-justify-content-center">
      <button class="button is-rounded is-dark mt-6" style="width: 120px;" @click="addTopicUser">Next</button>
    </div>
	</div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapMutations, mapGetters} from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';
import {ElMessage} from "element-plus";

@Options({
	data() {
    return {
      categories: [] as any,
			selectedList: []
    };
  },
  methods: {
		...mapMutations(["SET_LOADING"]),
		...mapActions("topic", [ActionTypes.FETCH_TOPICS]),
    ...mapActions("user", [ActionTypes.UPDATE_USER_CATEGORY]),

		async getCategory(){
      this.SET_LOADING(true)
      let data = await this.FETCH_TOPICS()
      if (data) {
        this.categories = data.results
      }
      this.SET_LOADING(false)
    },

    toggleCategory(category_id:any) {
			if(this.selectedList.includes(category_id)){
				this.selectedList = this.selectedList.filter((id:any) => id !== category_id);
			}
			else
				this.selectedList.push(category_id)
    },

    async addTopicUser(){
      let res = await this.UPDATE_USER_CATEGORY({user_id: this.userInfo.id, category_ids: {category_ids: this.selectedList}})
      if(res.status == 200)
        this.$router.push('/home')
      else
        ElMessage.error('Có lỗi đã xảy ra.')
    }
  },

  computed: {
    ...mapGetters("user", ["userInfo"]),
  },

	async created() {
    await this.getCategory()
    if(this.userInfo.categories.length != 0)
      for (const cate of this.userInfo.categories)
        this.selectedList.push(cate.id)
  },
})

export default class CategoryPage extends Vue {
}
</script>

<style lang="scss" scoped>
.detail-post {
  padding: 5% 30% 0% 30%;
  background-color: white;
  height: 100vh;
}
</style>