<template>
  <div class="detail-post" v-loading="loading">
    <div style="margin-bottom:50px;">
      <SummarySection :postDetail="postDetail"></SummarySection>
    </div>
    <div>
      <ContentSection v-if="!postDetail.description" :contents="postDetail.contents"></ContentSection>
      <div v-else>
        <div v-html="postDetail.description"></div>
      </div>
    </div>
    <div>
      <FooterSection :postDetail="postDetail"></FooterSection>
    </div>
    <div>
      <RecommendationSection></RecommendationSection>
    </div>
    <div class="mt-5">
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="BÌNH LUẬN" name="BÌNH LUẬN">
          <CommentSection :post="postDetail"></CommentSection>
        </el-tab-pane>
        <el-tab-pane label="ĐÁNH GIÁ" name="ĐÁNH GIÁ">
          <RatingSection :post_prop="postRating"></RatingSection>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapState, mapGetters, mapMutations} from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';
import SummarySection from './SummarySection.vue';
import ContentSection from './ContentSection.vue';
import RecommendationSection from './RecommendationSection.vue';
import CommentSection from './CommentSection.vue';
import RatingSection from './RatingSection.vue';
import FooterSection from './FooterSection.vue';

@Options({
  components: {
    SummarySection,
    ContentSection,
    RecommendationSection,
    CommentSection,
    FooterSection,
    RatingSection
  },

  data() {
    return {
      postDetail: {
        category: {
          title: ""
        },
        user: {
          id: ""
        }
      },
      postRating: {},
      loading: true,
      activeName: 'BÌNH LUẬN',
    }
  },

  methods: {
    ...mapMutations(["SET_LOADING"]),
    ...mapActions("post", [ActionTypes.FETCH_POST_DETAIL, ActionTypes.FETCH_POST_COMMENT_RATING]),

    async getPostDetail(){
      this.SET_LOADING(true)
      let data = await this.FETCH_POST_DETAIL(this.$route.params.slug)
      if (data) {
        this.postDetail = data
      }
      this.SET_LOADING(false)
    },
    async handleClick(){
      let data = await this.FETCH_POST_COMMENT_RATING(this.$route.params.slug)
      this.postRating = data
    }
  },

  watch: {
    async $route(){
      this.loading = true
			await this.getPostDetail()
      this.loading = false
		}
	},

  async created(){
    await this.getPostDetail()
    this.loading = false
  },

})

export default class PostDetailPage extends Vue {
}
</script>

<style lang="scss" scoped>
.detail-post {
  padding: 0% 20% 0% 20%;
}

:deep(.el-tabs__item){
  font-size: 20px !important;
}
</style>