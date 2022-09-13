<template>
  <div class="main-container p-2">
    <div class="campaign-container">
      <router-link to="/categories/management" class="button is-rounded btn-change">
        <font-awesome-icon icon="fa-solid fa-tags" class="mr-2"/>
        |
        <font-awesome-icon icon="fa-solid fa-chalkboard" class="ml-2 mr-2"/>
        Campaign Management
      </router-link>

      <el-row :gutter="20" class="mb-4 is-vcentered">
        <el-col :md="12" class="mb-2">
          <el-select-v2
            v-model="query.categories"
            :options="topics"
            placeholder="Categories"
            style="width: 100%; height: 100%"
            size="large"
            multiple
          />
        </el-col>

        <el-col :md="12" align="right">
          <el-radio-group
            v-model="query.status"
            size="large"
            style="height: 100%">
            <el-radio-button label="ALL"/>
            <el-radio-button :label="CAMPAIGN_STATUS.DRAFT"/>
            <el-radio-button :label="CAMPAIGN_STATUS.PUBLISHED"/>
<!--            <el-radio-button :label="CAMPAIGN_STATUS.DEACTIVATED"/>-->
          </el-radio-group>
        </el-col>
      </el-row>

      <el-row :gutter="20" v-show="!loading">
        <el-col :xl="8" :lg="8" :sm="12" :xs="24" v-for="campaign in campaigns">
          <CampaignItem :campaign="campaign" @deleteCampaign="getListCampaigns"></CampaignItem>
        </el-col>
      </el-row>
      <span v-if="loading" class="p-6 is-flex is-justify-content-center">
        <button class="button is-text" disabled style="text-decoration: none">
          <el-icon class="is-loading mr-2">
            <Loading/>
          </el-icon>
          Loading...
        </button>
      </span>
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
import {mapActions, mapMutations} from "vuex";
import CampaignItem from "@/components/CampaignItem.vue";
import {ActionTypes} from "@/types/store/ActionTypes";
import Campaign from "@/types/campaign/CampaignItem";
import Pagination from "@/components/Pagination.vue";
import {CAMPAIGN_STATUS} from "@/const/campaign_status";

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
        page_size: 11,
        q: "",
        status: "ALL",
        categories: []
      },
      topics: [],
      CAMPAIGN_STATUS: CAMPAIGN_STATUS,
      loading: false,
      timeOut: null,
      timer: 300,
    }
  },
  methods: {
    ...mapActions("campaign", [ActionTypes.FETCH_CAMPAIGN_MANAGEMENT]),
    ...mapActions("topic", [ActionTypes.FETCH_TOPICS]),
    ...mapMutations(["SET_LOADING"]),
    async getListCampaigns() {
      let data = await this.FETCH_CAMPAIGN_MANAGEMENT(this.query)
      if (data) {
        this.campaigns = data.results
        this.total = data.count
      } else {
        this.campaigns = []
        this.total = 0
      }
      this.campaigns.unshift({} as Campaign)
    },
    async getListTopics() {
      const data: any = await this.FETCH_TOPICS(this.query)
      this.topics = data.results.map((topic: any) => ({
        value: topic.id,
        label: topic.name,
      }))
    },
  },
  watch: {
    query: {
      deep: true,
      handler: async function () {
        this.loading = true
        this.$router.replace({query: this.query})
        await this.getListCampaigns();
        this.loading = false
      },
    },
    '$route.query.q': {
      handler() {
        this.query = this.$route.query
      },
      deep: true,
    }
  },
  async created() {
    this.loading = true
    await this.getListTopics()
    await this.getListCampaigns()
    this.loading = false
  },
  mounted() {
    document.title = 'Campaign Management | E-Learning'
  }
})

export default class CampaignManagementPage extends Vue {
}
</script>

<style scoped lang="scss">
.main-container {
  h1 {
    font-size: 1.3rem;
    color: #666;
    font-weight: 500;
  }

  .campaign-container {
    margin-bottom: 10px;
  }

  .btn-change {
    font-size: 0.95rem;
    font-weight: 450;
    margin-bottom: 25px;
  }
}
</style>
