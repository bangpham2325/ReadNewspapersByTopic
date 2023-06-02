<template>
  <el-row>
    <el-col :span=12>
      <h1 class="title is-3 is-flex">Tất cả bài viết</h1>
    </el-col>
    <el-col :span=12>
      <div class="is-flex is-justify-content-right">
        <el-radio-group v-model="filterStatus" size="large">
          <el-radio-button label="ALL" @change="handleRadioChange('ALL')"/>
          <el-radio-button label="DRAFT" @change="handleRadioChange('DRAFT')"/>
          <el-radio-button label="PUBLISHED" @change="handleRadioChange('PUBLISHED')"/>
        </el-radio-group>
      </div>
    </el-col>
  </el-row>
	
  <div class="tile is-ancestor layout-post">
    <template v-for="post in postsFiltered">
      <div class="tile is-parent" @click="detailPost(post.id)">
        <div class="tile is-child box card">
          <div class="card-image">
            <figure class="image is-3by2">
              <img :src=post.thumbnail alt="Placeholder image">
            </figure>
          </div>
          <div class="card-content">
            <el-row class="mb-3">
              <el-col :span="12">
								<el-row>
									<el-tag v-if="post.status=='DRAFT'" type="info" effect="dark">{{ post.status }}</el-tag>
									<el-tag v-else type="success" effect="dark">{{ post.status }}</el-tag>
								</el-row>
              </el-col>
              <el-col :span="12">
                <el-row class="is-flex is-justify-content-right">
									<p class="title is-6" style="color:#00773e;">{{ post.category.title }}</p>
                </el-row>
              </el-col>
            </el-row>

            <p class="title is-5" style="min-height:70px;">{{  post.title }}</p>
            <p style="color:#808080; font-size: 12px; min-height:100px;">{{ post.summary }}</p>

						<el-row>
							<el-col :span="14">
								<el-row>
										<el-avatar :size="40" class="mt-1">
											<img src="https://img.vietcetera.com/uploads/avatar-images/12-apr-2023/vu-hoang-long-1681282620604-160x160.jpg">
										</el-avatar>
										<p class="title is-6 mt-4 ml-4" style="color:#00773e;">{{ post.author }}</p>
								</el-row>
							</el-col>
					
							<el-col :span="10">
								<el-row class="is-flex is-justify-content-right">
									<p class="title is-6 mt-4">{{ post.publish_date }}</p>
								</el-row>
							</el-col>
						</el-row>
          </div>
        </div>
      </div>
    </template>
  </div> 

	<div class="is-flex is-justify-content-center mt-4">
		<el-pagination 
			background 
			layout="prev, pager, next" 
			:total=totalPage
			@current-change="handleCurrentChange"/>
	</div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapMutations } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";

@Options({
	data(){
    return {
      posts: [],
      postsFiltered: [],
			currentPage: 1,
      filterStatus: 'ALL',
      totalPage: 10
    }
  },

	methods: {
    ...mapMutations(["SET_LOADING"]),
    ...mapActions("post", [ActionTypes.FETCH_POSTS]),
	
		async getPosts(){
      this.SET_LOADING(true)
      let data = await this.FETCH_POSTS()
      if (data) {
        this.totalPage = Math.ceil(data.count/12)*10
        this.posts = data.results
      }
      this.SET_LOADING(false)
    },

    detailPost(post_id: string){
      this.$router.push({ name: 'detail-post', params: { id: post_id } })
    },

    handleRadioChange(type:string) {
      if(type == 'ALL'){
        this.postsFiltered = this.posts
        this.filterStatus = type
      }
      else if(type == 'DRAFT'){
        this.postsFiltered = []
        for (let i in this.posts){
          if(this.posts[i].status == 'DRAFT')
            this.postsFiltered.push(this.posts[i])
        }
        this.filterStatus = type
      }
      else{
        this.postsFiltered = []
        for (let i in this.posts){
          if(this.posts[i].status == 'PUBLISHED')
            this.postsFiltered.push(this.posts[i])
        }
        this.filterStatus = type
      }
    },

		async handleCurrentChange(currentPage:any) {
      this.currentPage = currentPage;
      let data = await this.FETCH_POSTS({page: this.currentPage})
      if (data) {
        this.posts = data.results
      }
      if(this.filterStatus == 'ALL')
        this.postsFiltered = this.posts
      else{
        this.postsFiltered = []
        for (let i in this.posts){
          if(this.posts[i].status == this.filterStatus)
            this.postsFiltered.push(this.posts[i])
        }
      }
			this.scrollToTop()
    },
		
		scrollToTop() {
			window.scrollTo({
				top: 0,
				behavior: 'smooth',
			});
		},
  },

	async created(){
    await this.getPosts()
    this.postsFiltered = this.posts
  },
})

export default class ManagementPage extends Vue {
  user!: any
}

</script>

<style lang="scss" scoped>
.tile.is-ancestor.layout-post{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 10px;
}
.el-radio-button {
  --el-radio-button-checked-bg-color:#00773e;
  --el-radio-button-checked-border-color: #00773e;
}
</style>