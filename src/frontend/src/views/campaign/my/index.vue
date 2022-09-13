<template>
  <div class="main-container p-2" v-show="!is_loading">
    <div class="campaign-container">
      <h1>Joined Campaigns</h1>
      <el-row :gutter="20">
        <el-col :xl="8" :lg="8" :sm="12" :xs="24" v-for="campaign in campaigns">
          <CampaignItem :campaign="campaign.event"></CampaignItem>
        </el-col>
      </el-row>
    </div>

    <Pagination
      :total="total"
      :page="query.page"
      :page_size="query.page_size"
      @changePage="query.page = $event">
    </Pagination>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import {mapActions, mapMutations, mapState} from "vuex";
import CampaignItem from "@/components/CampaignItem.vue";
import { ActionTypes } from "@/types/store/ActionTypes";
import Pagination from "@/components/Pagination.vue";

@Options({
  components: {
    Pagination,
    CampaignItem
  },
  data() {
    return {
      campaigns: [],
      total: 0,
      query: {
        page: 1,
        page_size: 6,
      },
    }
  },
  methods: {
    ...mapActions("campaign", [ActionTypes.FETCH_USER_CAMPAIGNS_PROCESS]),
    ...mapMutations(["SET_LOADING"]),
    async getListCampaigns() {
      this.SET_LOADING(true)
      let data = await this.FETCH_USER_CAMPAIGNS_PROCESS(this.query)
      this.campaigns = data.results
      this.total = data.count
      this.SET_LOADING(false)
    }
  },
  async created() {
    await this.getListCampaigns();
  },
  watch: {
    query: {
      deep: true,
      handler: async function () {
        await this.getListCampaigns();
        this.$router.replace({query: this.query}).catch((err: any) => err);
      },
    }
  },
  computed: {
    ...mapState(["is_loading"])
  },
  mounted() {
    document.title = 'My Campaign | E-Learning'
  }
})

export default class MyCampaignPage extends Vue {}
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
