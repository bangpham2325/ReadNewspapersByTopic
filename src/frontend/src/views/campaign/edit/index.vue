<template>
  <div class="main-container" style="max-width: 900px; margin: 0 auto">
    <TitleBar :title="title"></TitleBar>
    <div class="main-container__section has-background-white">
      <EditCampaign :campaign="campaign" :options="options"></EditCampaign>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import TitleBar from "@/components/TitleBar.vue";
import { mapActions, mapMutations } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElNotification } from "element-plus";
import TopicItem from "@/types/campaign/TopicItem";
import EditCampaign from "@/views/campaign/edit/EditCampaign.vue";

@Options({
  components: {
    EditCampaign,
    TitleBar,
  },
  data() {
    return {
      title: "Edit Campaign",
      options: [] as TopicItem[],
      campaign: {},
    };
  },
  methods: {
    ...mapActions("topic", [ActionTypes.FETCH_TOPICS]),
    ...mapActions("campaign", [ActionTypes.FETCH_CAMPAIGN_DETAIL]),
    ...mapMutations(["SET_LOADING"]),

    async fetchCampaign() {
      let event_types: any = await this.FETCH_TOPICS();
      let campaign: any = await this.FETCH_CAMPAIGN_DETAIL(this.$route.params.campaign_id);
      if (event_types && campaign) {
        this.options = event_types.results as TopicItem[];
        this.campaign = campaign;
        this.campaign.type_events = this.campaign.type_events.map(
          (event_type: TopicItem) => event_type.id
        );
      } else {
        ElNotification({
          title: "Error",
          message: "Loading data failed.",
          type: "error",
        });
      }
    },
  },
  async created() {
    this.SET_LOADING(true);
    await this.fetchCampaign();
    setTimeout(() => {
      this.SET_LOADING(false);
    }, 200);
  },
  mounted() {
    document.title = "Edit Campaign | E-Learning";
  },
})
export default class EditCampaignPage extends Vue {}
</script>

<style lang="scss" scoped>
.main-container {
  max-width: 900px;
  margin: 0 auto;

  &__section {
    border-radius: 20px;
    margin-bottom: 50px;
  }
}
</style>