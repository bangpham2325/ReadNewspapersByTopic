<template>
  <h1 class="title is-2 is-flex">Tin tức nổi bật</h1>
  <div class="tile is-ancestor">
    <div class="tile is-parent" @click="detailPost(postHot.id)">
      <div class="tile is-child box card">
        <div class="card-image">
          <figure class="image is-2by1" style="height:auto">
            <img :src=postHot.thumbnail alt="Placeholder image">
          </figure>
        </div>
        <div class="card-content">
          <p class="title is-4">{{  postHot.title }}</p>
          <p class="subtitle is-5" style="color:#808080">{{ postHot.summary }}</p>
          <el-row>
            <el-col :span="12">
              <el-row>
                  <el-avatar :size="50">
                    <img src="https://img.vietcetera.com/uploads/avatar-images/12-apr-2023/vu-hoang-long-1681282620604-160x160.jpg">
                  </el-avatar>
                  <p class="title is-5 mt-4 ml-4" style="color:#00773e;">{{ postHot.author }}</p>
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
      <div class="tile is-child box card" v-for="post in postLikes" style="display: flex;align-items: center;">
        <el-row @click="detailPost(post.id)">
          <el-col :span="6" class="mr-5">
            <figure class="image is-1by1" >
              <img :src=post.thumbnail alt="Placeholder image">
            </figure>
          </el-col>

          <el-col :span="15">
            <p class="title is-6">{{  post.title }}</p>
            <p style="color:#808080; font-size: 12px;">{{ post.summary }}</p>
          </el-col>
        </el-row>       
      </div>
    </div>
  </div>

  <h1 class="title is-3 is-flex mt-6">Bài viết phổ biến</h1>
  <div class="tile is-ancestor layout-post">
    <template v-for="post in postByLibrary.post_views">
      <div class="tile is-parent" @click="detailPost(post.id)">
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
                  <el-button type="text" icon="Pointer" style="color:#00773e;" size="large">{{ post.views }}</el-button>
                </el-row>
              </el-col>
            </el-row>

            <p class="title is-5" style="min-height:90px;">{{  post.title }}</p>
            <p style="color:#808080; font-size: 12px; min-height:120px;">{{ post.summary }}</p>

            <el-row>
              <el-col :span="12">
                <el-button type="text" icon="Histogram" style="color:black;" size="large" class="title is-6 mt-1" v-if="post.avg_rating != null">{{ post.avg_rating }}</el-button>
                <el-button type="text" icon="Histogram" style="color:black;" size="large" class="title is-6 mt-1" v-else>0</el-button>
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
      <div class="tile is-parent" @click="detailPost(post.id)">
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
                  <el-button type="text" icon="StarFilled" style="color:#00773e;" size="large">{{ post.likes }}</el-button>
                </el-row>
              </el-col>
            </el-row>

            <p class="title is-5" style="min-height:90px;">{{  post.title }}</p>
            <p style="color:#808080; font-size: 12px;min-height:120px;">{{ post.summary }}</p>

            <el-row>
              <el-col :span="12">
                <el-button type="text" icon="Histogram" style="color:black;" size="large" class="title is-6 mt-1" v-if="post.avg_rating != null">{{ post.avg_rating }}</el-button>
                <el-button type="text" icon="Histogram" style="color:black;" size="large" class="title is-6 mt-1" v-else>0</el-button>
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
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapState, mapGetters, mapMutations} from "vuex";
import TopBar from "@/components/TopBar.vue";
import {MutationTypes} from "@/types/store/MutationTypes";
import { ActionTypes } from '@/types/store/ActionTypes';

@Options({
  components: {
    TopBar,
  },
  data(){
    return {
      postByLibrary: [],
      postLikes: [],
      postHot: {},
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

    detailPost(post_id: string){
      this.$router.push({ name: 'detail-post', params: { id: post_id } })
    }
  },

  async created(){
    await this.getPostByLibrary()
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
