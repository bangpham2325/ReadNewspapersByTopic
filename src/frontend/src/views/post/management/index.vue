<template>
  <el-row>
    <el-col :span=12>
      <h1 class="title is-3 is-flex">Tất cả bài viết</h1>
    </el-col>
    <el-col :span=12>
      <div class="is-flex is-justify-content-right">
        <el-radio-group v-model="filterStatus" size="large">
          <el-radio-button label="ALL" @change="handleRadioChange('ALL')" />
          <el-radio-button label="DRAFT" @change="handleRadioChange('DRAFT')" />
          <el-radio-button label="PENDING" @change="handleRadioChange('PENDING')" />
          <el-radio-button label="PUBLISHED" @change="handleRadioChange('PUBLISHED')" />
        </el-radio-group>
        <button v-if="(this.filterStatus == 'DRAFT' || this.filterStatus == 'PENDING') && this.userInfo.role == 'ADMIN' && !this.selectMuti"
          class="button is-primary ml-4" style="background-color: #00773e;" @click="selectMulPost">Chọn nhiều
          bài</button>
        <button v-if="this.selectMuti" class="button is-primary ml-4" style="background-color: #00773e;"
          @click="publishPosts">Đăng bài</button>
        <button v-if="this.selectMuti" class="button is-dark ml-4" @click="this.selectMuti = false">Hủy chọn
          nhiều</button>
        <button v-if="this.userInfo.role == 'AUTHOR'" class="button is-primary ml-4" style="background-color: #00773e;" @click="addPost">
          Tạo bài viết
        </button>
      </div>
    </el-col>
  </el-row>

  <div v-loading="loading">
    <div class="tile is-ancestor layout-post">
      <template v-for="post in posts">
        <div :class="['tile', 'is-parent']" @click="clickPost(post.slug, post.id, post.status)">
          <div :class="['tile', 'is-child', 'box card', { 'clickedPost': selectedPosts.includes(post.id) }]">
            <div class="card-image">
              <figure class="image is-3by2">
                <img v-if="post.thumbnail" :src=post.thumbnail alt="Placeholder image">
                <img v-else src="https://bulma.io/images/placeholders/800x480.png">
              </figure>
            </div>
            <div class="card-content">
              <el-row class="mb-3">
                <el-col :span="12">
                  <el-row>
                    <el-tag v-if="post.status == 'DRAFT'" type="info" effect="dark">{{ post?.status }}</el-tag>
                    <el-tag v-else-if="post.status == 'PENDING'" type="warning" effect="dark">{{ post?.status }}</el-tag>
                    <el-tag v-else type="success" effect="dark">{{ post?.status }}</el-tag>

                    <el-popover :width="900" placement="bottom">
                      <template #reference>
                        <el-button icon="Tickets" text circle class="ml-2"></el-button>
                      </template>
                      <template #default>
                        <el-scrollbar height="400px">
                          <div class="mx-6 my-6 px-6">
                            <div style="margin-bottom:50px;">
                              <el-row>
                                <el-col :span="12">
                                  <el-tooltip :content=post?.publish_date placement="top-start">
                                    <p class="title is-6" style="color:#808080">{{ post?.publish_date }}</p>
                                  </el-tooltip>
                                </el-col>
                                <el-col :span="12">
                                  <el-row class="is-flex is-justify-content-right">
                                    <el-tag v-if="post.status == 'DRAFT'" type="info" effect="dark">{{ post?.status }}</el-tag>
                                    <el-tag v-else-if="post.status == 'PENDING'" type="warning" effect="dark">{{ post?.status }}</el-tag>
                                    <el-tag v-else type="success" effect="dark">{{ post?.status }}</el-tag>
                                  </el-row>
                                </el-col>
                              </el-row>
                              <p class="title is-6" style="color:#00773e">{{ post.category?.title ? post.category.title : "" }}</p>
                              <h1 class="title is-4">{{ post?.title }}</h1>
                              <p class="subtitle is-6 mt-1" style="color:#808080">{{ post?.summary }}</p>
                              <el-row>
                                <el-col :span="12">
                                  <el-row>
                                    <el-avatar :size="40">
                                      <img :src="post.user ? post.user.avatar :'https://res.cloudinary.com/ddrpryfpq/image/upload/v1686479489/preview_unebjy.png'">
                                    </el-avatar>
                                    <p class="title is-6 mt-4 ml-4" style="color:#00773e;">{{ post?.author }}</p>
                                  </el-row>
                                </el-col>
                              </el-row>
                            </div>
                            
                            <div v-if="!post.description" v-for="content in post.contents">
                              <h2 class="title is-3">{{ content.title }}</h2>
                          
                              <div v-if="content.image && content.paragraph.length == 0">
                                <figure class="image is-2by1 my-3 custom-image">
                                  <img :src=content.image>
                                </figure>
                                <p class="subtitle is-6 is-flex is-justify-content-center has-text-centered"><b><i>{{ content.description_img }}</i></b></p>
                              </div>
                          
                              <div v-for="line in content.paragraph">
                                <p class="my-3">{{ line.text }}</p>
                                <div v-if="line.below_img">
                                  <figure class="image is-2by1 my-3">
                                    <img :src=content.image class="custom-image">
                                  </figure>
                                  <p class="subtitle is-6 is-flex is-justify-content-center has-text-centered"><b><i>{{ content.description_img }}</i></b></p>
                                </div>
                                
                              </div>
                            </div>

                            <div v-else>
                              <div v-html="post.description" class="img-content"></div>
                            </div>
                            <div>
                              <el-row>
                                <el-col :span="12">
                                  <el-tag class="mr-4" size="large" v-for="tag in post.keywords">{{ tag.keyword }}</el-tag>
                                </el-col>
                              </el-row>
                            </div>
                          </div>
                        </el-scrollbar>
                      </template>
                    </el-popover>
                  </el-row>
                </el-col>
                <el-col :span="12">
                  <el-row class="is-flex is-justify-content-right">
                    <p class="title is-6" style="color:#00773e;">{{ post.category?.title ? post.category.title : "" }}</p>
                  </el-row>
                </el-col>
              </el-row>

              <p class="title is-5" style="min-height:70px;">{{ post?.title }}</p>
              <p style="color:#808080; font-size: 12px; min-height:100px;">{{ post?.summary }}</p>

              <el-row>
                <el-col :span="14">
                  <el-row v-if="post.user">
                    <el-avatar :size="40" class="mt-1">
                      <img :src="post.user.avatar">
                    </el-avatar>
                    <p class="title is-6 mt-4 ml-4" style="color:#00773e;">{{ post?.author ? post.author : post.user.full_name }}</p>
                  </el-row>

                  <el-row v-else>
                    <el-avatar :size="40" class="mt-1">
                      <img src="@/assets/vectors/default_avatar.svg">
                    </el-avatar>
                    <p class="title is-6 mt-4 ml-4" style="color:#00773e;">{{ post?.author }}</p>
                  </el-row>
                </el-col>

                <el-col :span="10">
                  <el-row class="is-flex is-justify-content-right">
                    <p class="title is-6 mt-4">{{ post?.publish_date }}</p>
                  </el-row>
                </el-col>
              </el-row>
            </div>
          </div>
        </div>
      </template>
    </div>

    <div class="is-flex is-justify-content-center mt-4">
      <el-pagination background layout="prev, pager, next" :total=totalPage @current-change="handleCurrentChange" />
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapMutations, mapGetters } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElMessage } from "element-plus";
import Posts from '@/types/post/PostItem';

@Options({
  data() {
    return {
      posts: [] as Posts[],
      currentPage: 1,
      filterStatus: 'ALL',
      totalPage: 10,
      selectMuti: false,
      selectedPosts: [] as any,
      loading: true,
    }
  },

  methods: {
    ...mapMutations(["SET_LOADING"]),
    ...mapActions("post", [ActionTypes.FETCH_POSTS, ActionTypes.MY_POSTS, ActionTypes.PUBLISH_LIST_POST]),

    async getPosts(page: any = null, status: any = null) {
      this.SET_LOADING(true)
      let data: any
      if (this.userInfo.role === "ADMIN") {
        data = await this.FETCH_POSTS({page: page, status: status});
      } 
      else if (this.userInfo.role === "AUTHOR") {
        data = await this.MY_POSTS({page: page, status: status});
      }


      if (data) {
        this.totalPage = Math.ceil(data.count / 12) * 10
        this.posts = data.results
      }
      this.SET_LOADING(false)
    },
    detailPost(post_slug: string) {
      this.$router.push({ name: 'detail-post', params: { slug: post_slug } })
    },

    addPost(){
      this.$router.push("/post/add-post/")
    },

    async handleRadioChange(type: string) {
      if (type == 'ALL') {
        await this.getPosts()
        this.filterStatus = type
      }
      else {
        await this.getPosts(null, type)
        this.filterStatus = type
      }
    },

    async handleCurrentChange(currentPage: any) {
      this.currentPage = currentPage;
      if (this.filterStatus == 'ALL') {
        await this.getPosts(this.currentPage)
      }
      else
        await this.getPosts(this.currentPage, this.filterStatus)
      this.scrollToTop()
    },

    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    },

    selectMulPost() {
      this.selectedPosts = []
      this.selectMuti = true
    },

    clickPost(post_slug: string, post_id: string, post_status: string) {
      if (!this.selectMuti){
        if(post_status == 'DRAFT' && this.userInfo.role == 'AUTHOR')
          this.$router.push({ name: 'edit-post', params: { slug: post_slug }})
        else
          this.detailPost(post_slug)
      }
      else {
        if (this.selectedPosts.includes(post_id))
          this.selectedPosts = this.selectedPosts.filter((id: any) => id !== post_id);
        else
          this.selectedPosts.push(post_id)
      }
    },

    async publishPosts() {
      let res = await this.PUBLISH_LIST_POST({ post_ids: this.selectedPosts })
      if (res.status == 200) {
        await this.getPosts(this.currentPage, this.filterStatus)
        this.selectedPosts = []
        ElMessage({
          message: `Đăng bài thành công.`,
          type: 'success',
        })
      }
      else {
        ElMessage.error('Có lỗi đã xảy ra.')
      }
    }
  },
  computed: {
      ...mapGetters("user", ["userInfo"]),
  },
  async created() {
    await this.getPosts()
    this.loading = false
  },
})

export default class ManagementPage extends Vue {
  user!: any
}

</script>

<style lang="scss" scoped>
.tile.is-ancestor.layout-post {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 10px;
}

.el-radio-button {
  --el-radio-button-checked-bg-color: #00773e;
  --el-radio-button-checked-border-color: #00773e;
}

.clickedPost {
  border: 3px solid #00773e;
}

:deep(.ql-align-center){
	text-align: center;
}

:deep(.ql-align-right){
	text-align: right;
}

.custom-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}


:deep(.img-content p img){
  display: block;
  margin: auto auto;
}
</style>