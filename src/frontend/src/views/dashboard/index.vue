<template>
	<div class="main-container p-2">
    <div class="campaign-container">
      <h1>New Campaign</h1>
      <el-row :gutter="40">
        <el-col :xl="8" :lg="8" :sm="12" :xs="24" v-for="campaign in campaigns">
          <CampaignItem :campaign="campaign"></CampaignItem>
        </el-col>
      </el-row>
    </div>

    <div class="campaign-container">
      <h1>Most Popular</h1>
      <el-row :gutter="40">
        <el-col :xl="8" :lg="8" :sm="12" :xs="24" v-for="campaign in campaigns">
          <CampaignItem :campaign="campaign"></CampaignItem>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from "vue-class-component";
import {mapActions, mapMutations} from "vuex";
import CampaignItem from "@/components/CampaignItem.vue";
import {ActionTypes} from "@/types/store/ActionTypes";
import Campaign from "@/types/campaign/CampaignItem";

@Options({
  components: {
    CampaignItem
  },
	data() {
    return {
      campaigns: [] as Campaign[],
      total: 0,
      query: {
        page: 1,
        page_size: 6,
      },
    }
  },
	methods: {
    ...mapActions("campaign", [ActionTypes.FETCH_CAMPAIGNS]),
    ...mapMutations(["SET_LOADING"]),
    async getListCampaign() {
      this.SET_LOADING(true)
      let data = await this.FETCH_CAMPAIGNS(this.query)
      this.campaigns = data.results as Campaign[]
      this.SET_LOADING(false)
    }
  },
  async created() {
    await this.getListCampaign();
  },
  mounted() {
    document.title = 'Dashboard | V-Volunteer'
  }
})

export default class DashboardPage extends Vue {
}
</script>

<style scoped lang="scss">
.main-container {
  h1 {
    font-size: 1.22rem;
    margin-bottom: 20px;
    color: #666;
    font-weight: 500;
  }

  .campaign-container {
    margin-bottom: 10px;
  }
}
</style>