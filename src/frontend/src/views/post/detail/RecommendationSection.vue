<template>
  <div v-if="postCommendation.length != 0">
    <h2 class="title is-2 my-6">ĐỪNG BỎ LỠ</h2>
    
    <el-carousel :interval="5000" type="card" height="300px" v-if="postCommendation.length >= 3">
      <el-carousel-item v-for="item in postCommendation" :key="item">
        <div class="carousel-item-container" @click="detailPost(item.id)">
          <img :src="item.thumbnail" :alt="item.title" />
          <h3 class="title is-6 mt-4">{{ item.title }}</h3>
        </div>
      </el-carousel-item>
    </el-carousel>

    <el-carousel :interval="5000" arrow="always" height="330px" v-else>
      <el-carousel-item v-for="item in postCommendation" :key="item">
        <div class="carousel-item-container" style="display: flex;flex-direction: column;align-items: center;" @click="detailPost(item.id)">
          <img :src="item.thumbnail" :alt="item.title"/>
          <h3 class="title is-6 mt-4">{{ item.title }}</h3>
        </div>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import { mapActions, mapMutations } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import {ElMessage} from "element-plus";

@Options({
  data(){
    return {
      postCommendation: [] as any
    }
  },

  methods: {
    ...mapMutations(["SET_LOADING"]),
    ...mapActions("post", [ActionTypes.RECOMENDATION_POST]),

    async getPostRecommendation(){
      this.SET_LOADING(true)
      let data = await this.RECOMENDATION_POST(this.$route.params.id)
      if(data)
        this.postCommendation = data.message
      console.log(this.postCommendation)
      this.SET_LOADING(false)
    },

    detailPost(post_id: string){
      this.$router.push({ name: 'detail-post', params: { id: post_id } })
    },
  },

  async created(){
    await this.getPostRecommendation()
  },

})

export default class RecommendationSection extends Vue {
}
</script>

<style scoped>
.el-carousel__item h3 {
  opacity: 0.75;
  margin: 0;
  text-align: center;
  position: absolute;
  top: 80%;
  color: white;
  background-color: rgba(0, 0, 0, 0.9);
  padding: 5px 10px;
}

.carousel-item-container {
  position: relative;
}

</style>