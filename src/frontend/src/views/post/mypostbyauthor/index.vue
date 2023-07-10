<template>
  <div v-loading="loading">
    <el-row>
      <el-col :span=12>
        <h1 class="title is-3 is-flex">Tất cả bài viết cuả {{ posts[0]?.user.full_name }}</h1>
      </el-col>
    </el-row>

    <div class="tile is-ancestor layout-post">
      <template v-for="post in posts">
        <div :class="['tile', 'is-parent']" @click="clickPost(post.slug)">
          <div :class="['tile', 'is-child', 'box card']">
            <div class="card-image">
              <figure class="image is-3by2">
                <img :src=post.thumbnail alt="Placeholder image">
              </figure>
            </div>
            <div class="card-content">
              <el-row class="mb-3">
                <el-col :span="12">
                  <el-row>
                    <el-tag type="success" effect="dark">{{ post?.status }}</el-tag>
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
                  <el-row>
                    <el-avatar :size="40" class="mt-1">
                      <img :src="post.user ? post.user.avatar : 'https://res.cloudinary.com/ddrpryfpq/image/upload/v1686479489/preview_unebjy.png'">
                    </el-avatar>
                    <p class="title is-6 mt-4 ml-4" style="color:#00773e;">{{ post?.user.full_name }}</p>
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
import { mapActions, mapMutations, mapGetters, mapState } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElMessage } from "element-plus";

@Options({
  data() {
    return {
      posts: [],
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
    ...mapActions("post", [ActionTypes.FETCH_POSTS_BY_AUTHOR]),

    async getPostByCategory() {
      this.SET_LOADING(true)
      let data = await this.FETCH_POSTS_BY_AUTHOR({ user_id: this.$route.params.id })
      if (data) {
        this.posts = data
      }
      this.SET_LOADING(false)
    },
    clickPost(post_slug: string) {
      this.$router.push({ name: 'detail-post', params: { slug: post_slug } })
    },
  },

  async created() {
    await this.getPostByCategory()
    this.loading = false
  },
  computed: {
    ...mapGetters("user", ["userInfo"]),
  },
})

export default class MyPostByAuthor extends Vue {
  user!: any
}

</script>

<style lang="scss" scoped>
.tile.is-ancestor.layout-post {
  display: grid;
  grid-template-columns: repeat(3, auto);
  grid-gap: 10px;
}

.el-radio-button {
  --el-radio-button-checked-bg-color: #00773e;
  --el-radio-button-checked-border-color: #00773e;
}

.clickedPost {
  border: 3px solid #00773e;
}
</style>