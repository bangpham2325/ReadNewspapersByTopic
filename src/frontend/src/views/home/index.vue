<template>
  <div v-loading="loading">
    <h1 class="title is-2 is-flex">Tin tức nổi bật</h1>
    <div class="tile is-ancestor">
      <div class="tile is-parent" @click="detailPost(postHot.slug)">
        <div class="tile is-child box card">
          <div class="card-image">
            <figure class="image is-2by1" style="height:auto;">
              <img :src=postHot.thumbnail alt="Placeholder image">
            </figure>
          </div>
          <div class="card-content">
            <p class="title is-5">{{  postHot.title }}</p>
            <p class="subtitle is-6" style="color:#808080">{{ postHot.summary }}</p>
            <el-row>
              <el-col :span="12">
                <el-row>
                    <el-avatar :size="45">
                      <img src="https://img.vietcetera.com/uploads/avatar-images/12-apr-2023/vu-hoang-long-1681282620604-160x160.jpg">
                    </el-avatar>
                    <p class="title is-6 mt-4 ml-4" style="color:#00773e;">{{ postHot.author }}</p>
                </el-row>
              </el-col>
          
              <el-col :span="12">
                <el-row class="is-flex is-justify-content-right">
                  <p class="title is-6 mt-4">{{ postHot.publish_date }}</p>
                </el-row>
              </el-col>
            </el-row>
          </div>    
        </div>
      </div>

      <div class="tile is-5 is-vertical is-parent">
        <div class="tile is-child box card" v-for="post in postLikes" style="display: flex;align-items: center">
          <el-row @click="detailPost(post.slug)">
            <el-col :span="6" class="mr-5" style="background:#f1f1f1;display: flex;align-items: center">
              <figure class="image mt-3" style="width: 100%; height:auto">
                <img :src=post.thumbnail alt="Placeholder image">
              </figure>
            </el-col>

            <el-col :span="15">
              <p class="title is-6 mb-3">{{  post.title }}</p>
              <p style="color:#808080; font-size: 12px;">{{ post.summary }}</p>
            </el-col>
          </el-row>       
        </div>
      </div>
    </div>

    <h1 class="title is-3 is-flex mt-6">Bài viết phổ biến</h1>
    <div class="tile is-ancestor layout-post">
      <template v-for="post in postByLibrary.post_views">
        <div class="tile is-parent" @click="detailPost(post.slug)">
          <div class="tile is-child box card">
            <div class="card-image">
              <figure class="image is-3by2">
                <img :src=post.thumbnail alt="Placeholder image">
              </figure>
            </div>
            <div class="card-content">
              
              <el-row>
                <el-col :span="20">
                  <el-row>
                    <p class="title is-6 mt-3" style="color:#00773e;">{{ post.category.title }}</p>
                  </el-row> 
                </el-col>
                <el-col :span="4">
                  <el-row class="is-flex is-justify-content-right">
                    <el-button type="text" icon="View" style="color:#00773e;padding:0 !important" size="large">{{ post.views }}</el-button>
                  </el-row>
                </el-col>
              </el-row>

              <p class="title mb-1" style="min-height:90px;font-size:18px">{{  post.title }}</p>
              <p style="color:#808080; font-size: 12px; min-height:100px;">{{ post.summary }}</p>

              <el-row>
                <el-col :span="12">
                  <el-button type="text" icon="Star" style="color:black;padding:0 !important" size="large" class="title is-6 mt-1" v-if="post.avg_rating != null">{{ post.avg_rating }}/5</el-button>
                  <el-button type="text" icon="Star" style="color:black;padding:0 !important" size="large" class="title is-6 mt-1" v-else>0/5</el-button>
                </el-col>
                <el-col :span="12">
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

    <h1 class="title is-3 is-flex mt-6">Bài viết được yêu thích</h1>

    <div class="tile is-ancestor layout-post">
      <template v-for="post in postByLibrary.post_favourite">
        <div class="tile is-parent" @click="detailPost(post.slug)">
          <div class="tile is-child box card">
            <div class="card-image">
              <figure class="image is-3by2">
                <img :src=post.thumbnail alt="Placeholder image">
              </figure>
            </div>

            <div class="card-content">

              <el-row>
                <el-col :span="20">
                  <el-row>
                    <p class="title is-6 mt-3" style="color:#00773e;">{{ post.category.title }}</p>
                  </el-row> 
                </el-col>
                <el-col :span="4">
                  <el-row class="is-flex is-justify-content-right">
                    <el-button type="text" size="large" style="padding:0 !important; color: #00773e;"><font-awesome-icon :icon="['fas', 'thumbs-up']" style="color: #00773e;" class="mr-2" />{{ post.likes }}</el-button>
                  </el-row>
                </el-col>
              </el-row>

              <p class="title is-5" style="min-height:90px;">{{  post.title }}</p>
              <p style="color:#808080; font-size: 12px;min-height:120px;">{{ post.summary }}</p>

              <el-row>
                <el-col :span="12">
                  <el-button type="text" icon="Star" style="color:black;padding:0 !important" size="large" class="title is-6 mt-1" v-if="post.avg_rating != null">{{ post.avg_rating }}/5</el-button>
                  <el-button type="text" icon="Star" style="color:black;padding:0 !important" size="large" class="title is-6 mt-1" v-else>0/5</el-button>
                </el-col>
                <el-col :span="12">
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
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapState, mapGetters, mapMutations} from "vuex";
import TopBar from "@/components/TopBar.vue";
import {MutationTypes} from "@/types/store/MutationTypes";
import { ActionTypes } from '@/types/store/ActionTypes';
import Posts from '@/types/post/PostItem';

@Options({
  components: {
    TopBar,
  },
  data(){
    return {
      postByLibrary: [] as Posts[],
      postLikes: [] as Posts[],
      postHot: {} as Posts,
      loading: true,
      categories: [],
    }
  },

  methods: {
    ...mapMutations(["SET_LOADING"]),
    ...mapActions("post", [ActionTypes.FETCH_POST_LIBRARY]),

    async getPostByLibrary(){
      this.SET_LOADING(true)
      let data = await this.FETCH_POST_LIBRARY()
      if (data) {
        this.postByLibrary = data
        this.postHot = this.postByLibrary.post_likes[0]
        for(let i = 1; i < 4; i++){
          this.postLikes[i-1] = this.postByLibrary.post_likes[i]
        }
      }
      this.SET_LOADING(false)
    },

    detailPost(post_slug: string){
      this.$router.push({ name: 'detail-post', params: { slug: post_slug } })
    }
  },

  computed: {
    ...mapState(["is_loading"]),
    ...mapGetters("user", ["userInfo"]),
  },

  async created(){
    await this.getPostByLibrary()
    this.loading = false
  },

  mounted() {
    document.title = 'Home | New Portal'
  }
})

export default class HomePage extends Vue {
}


</script>

<style lang="scss">
@import "@/views/home/style.scss";
.tile.is-ancestor.layout-post{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 10px;
}
</style>
