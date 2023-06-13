<template>
  <div class="detail-post" v-loading="loading">
    <div style="margin-bottom:50px;">
      <SummarySection :postDetail="postDetail"></SummarySection>
    </div>
    <div>
      <ContentSection :contents="postDetail.contents"></ContentSection>
    </div>
    <div>
      <FooterSection :postDetail="postDetail"></FooterSection>
    </div>
    <div>
      <RecommendationSection></RecommendationSection>
    </div>
    <div>
      <CommentSection :post="postDetail"></CommentSection>
      <RatingSection :post="postDetail"></RatingSection>
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
      loading: true,
    }
  },

  methods: {
    ...mapMutations(["SET_LOADING"]),
    ...mapActions("post", [ActionTypes.FETCH_POST_DETAIL]),

    async getPostDetail(){
      this.SET_LOADING(true)
      let data = await this.FETCH_POST_DETAIL(this.$route.params.id)
      if (data) {
        this.postDetail = data
      }
      this.SET_LOADING(false)
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
</style>