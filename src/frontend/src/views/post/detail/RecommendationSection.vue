<template>
  <div v-if="postCommendation.length != 0">
    <h2 class="title is-2 my-6">ĐỪNG BỎ LỠ</h2>
    <div class="carousel-container">
      <el-carousel :interval="5000" arrow="always" height="300" >
        <el-carousel-item v-for="(chunk, index) in postChunks" :key="index">
          <div class="tile is-ancestor carousel-item">
              <div v-for="post in chunk" :key="post.id">
                <div class="tile is-parent" @click="detailPost(post.slug)">
                  <div class="tile is-child box card" style="min-height:280px">
                    <div class="card-image">
                      <figure class="image is-3by2">
                        <img :src="post.thumbnail" :alt="post.title" alt="Placeholder image">
                      </figure>
                      <h3 class="title is-6 mt-4">{{ post.title }}</h3>
                    </div>
                  </div>
                </div>
              </div>
            </div>
        </el-carousel-item>
      </el-carousel>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapMutations } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElMessage } from "element-plus";

@Options({
  data() {
    return {
      postCommendation: [] as any,
    }
  },

  methods: {
    ...mapMutations(["SET_LOADING"]),
    ...mapActions("post", [ActionTypes.RECOMENDATION_POST]),

    async getPostRecommendation() {
      this.SET_LOADING(true)
      let data = await this.RECOMENDATION_POST(this.$route.params.slug)
      if (data)
        this.postCommendation = data.message
      this.SET_LOADING(false)
    },

    detailPost(post_slug: string) {
      this.$router.push({ name: 'detail-post', params: { slug: post_slug } })
    },
  },

  computed: {
    postChunks() {
      const chunks = [];
      const postsCopy = [...this.postCommendation];
      while (postsCopy.length) {
        chunks.push(postsCopy.splice(0, 3));
      }
      return chunks;
    }
  },

  async created() {
    await this.getPostRecommendation()
  },

})

export default class RecommendationSection extends Vue {
}
</script>

<style scoped>
.carousel-item {
  display: flex;
  justify-content: space-between;
}

.tile.is-ancestor{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 10px;
}

</style>