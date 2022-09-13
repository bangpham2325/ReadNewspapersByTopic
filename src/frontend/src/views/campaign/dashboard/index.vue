<template>
  <div class="main-container p-2" v-show="!is_loading">
    <div class="campaign-container">
      <h1>Campaigns</h1>
      <el-row :gutter="40">
        <el-col :xl="8" :lg="8" :sm="12" :xs="24" v-for="campaign in campaigns">
          <CampaignItem :campaign="campaign"></CampaignItem>
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
import {Options, Vue} from "vue-class-component";
import {mapActions, mapMutations, mapState} from "vuex";
import CampaignItem from "@/components/CampaignItem.vue";
import {ActionTypes} from "@/types/store/ActionTypes";
import Campaign from "@/types/campaign/CampaignItem";
import Pagination from "@/components/Pagination.vue";

@Options({
  components: {
    CampaignItem,
    Pagination
  },
  data() {
    return {
      campaigns: [] as Campaign[],
      total: 0,
      query: {
        page: 1,
        page_size: 12,
      },
    }
  },
  computed: {
    ...mapState(["is_loading"])
  },
  methods: {
    ...mapActions("campaign", [ActionTypes.FETCH_CAMPAIGNS]),
    ...mapMutations(["SET_LOADING"]),
    async getListCampaign() {
      this.SET_LOADING(true)
      let data = await this.FETCH_CAMPAIGNS(this.query)
      this.campaigns = data.results as Campaign[]
      this.total = data.count
      this.SET_LOADING(false)
    }
  },
  watch: {
    query: {
      deep: true,
      handler: async function () {
        await this.getListCampaign();
        this.$router.replace({query: this.query}).catch((err: any) => err);
      },
    },
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