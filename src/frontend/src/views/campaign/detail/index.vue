<template>
  <div class="main-container" v-show="!is_loading">
    <TitleBar :title="campaign.title"></TitleBar>

    <div class="campaign-detail__background">
      <CoverImage :image="campaign.background" :is_freeze="true"></CoverImage>
    </div>

    <div class="campaign-detail p-3">
      <InfoSection
        :campaign="campaign"
        @addRating="handleAddRating"
        @updateStatus="registerStatus = $event"
      >
      </InfoSection>
    </div>

    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo pl-5"
      mode="horizontal"
      style="border-radius:15px 15px 0 0;">
      <el-menu-item index="1" @click="changeTab('Newsfeed')">
        <font-awesome-icon icon="fa-regular fa-newspaper" class="mr-2"/>
        Newsfeed
      </el-menu-item>
      <el-menu-item v-show="registerStatus == PROCESS_STATUS.REGISTERED" index="2" @click="changeTab('Member')">
        <font-awesome-icon icon="fa-solid fa-users" class="mr-2"/>
        Member
      </el-menu-item>
      <el-menu-item index="3" @click="changeTab('Information')">
        <font-awesome-icon icon="fa-solid fa-circle-info" class="mr-2"/>
        Information
      </el-menu-item>
      <el-menu-item v-show="registerStatus == PROCESS_STATUS.REGISTERED" index="4" @click="changeTab('Donation')">
        <font-awesome-icon icon="fa-solid fa-circle-dollar-to-slot" class="mr-2"/>
        Donation
      </el-menu-item>
      <el-menu-item v-show="registerStatus == PROCESS_STATUS.REGISTERED" index="5" @click="changeTab('Rating')">
        <font-awesome-icon icon="fa-regular fa-star" class="mr-2"/>
        Rating
      </el-menu-item>
      <el-menu-item v-show="registerStatus == PROCESS_STATUS.REGISTERED" index="6" @click="changeTab('Chat')">
        <font-awesome-icon icon="fa-regular fa-comments" class="mr-2"/>
        Chat
      </el-menu-item>
    </el-menu>
    <ActivitySection
      v-if="(tab=='Newsfeed')"
      :campaign="campaign"
      :is-auth="isAuth"
      :register-status="registerStatus"
      class="p-5"
      @addPost="this.campaign.post_events.unshift($event)"
    ></ActivitySection>
    <MemberSection v-if="(tab =='Member')" :campaign="campaign"></MemberSection>
    <DescriptionSection v-if="(tab=='Information')" :description="campaign.description"></DescriptionSection>
    <DonationSection v-if="(tab=='Donation')" :campaign="campaign" @addTransaction="handleAddTransaction"></DonationSection>
    <RatingSection v-if="(tab=='Rating')" :campaign="campaign"></RatingSection>
    <ChatSection v-if="(tab=='Chat')" :chat-room-id="this.campaign.room_uri"></ChatSection>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import InfoSection from './InfoSection.vue'
import DescriptionSection from './DescriptionSection.vue'
import ActivitySection from "./ActivitySection.vue";
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import {ActionTypes} from "@/types/store/ActionTypes";
import TitleBar from "@/components/TitleBar.vue";
import CoverImage from "@/components/CoverImage.vue";
import RatingSection from "./RatingSection.vue";
import MemberSection from "./MemberSection.vue";
import {PROCESS_STATUS} from "@/const/process_status";
import ChatSection from "@/views/campaign/detail/ChatSection.vue";
import DonationSection from "@/views/campaign/detail/DonationSection.vue";

@Options({
  components: {
    DonationSection,
    ChatSection,
    TitleBar,
    ActivitySection,
    InfoSection,
    DescriptionSection,
    CoverImage,
    RatingSection,
    MemberSection
  },
  data() {
    return {
      PROCESS_STATUS: PROCESS_STATUS,
      campaign: {
        id: "",
        post_events: [
          {
            "id": "",
            "title": "",
            "description": "",
            "images": []
          }
        ],
        user: {
          full_name: ""
        },
        room_uri: ""
      } as any,
      activeIndex: "1",
      tab: 'Newsfeed',
      isAuth: false,
      registerStatus: PROCESS_STATUS.UNREGISTER
    }
  },
  methods: {
    ...mapActions('campaign', [ActionTypes.FETCH_CAMPAIGN_DETAIL]),
    ...mapActions('campaignProcess', [ActionTypes.FETCH_CAMPAIGN_PROCESS_DETAIL]),
    ...mapMutations(["SET_LOADING"]),
    async getCampaignDetail() {
      this.SET_LOADING(true)
      let data = await this.FETCH_CAMPAIGN_DETAIL(this.$route.params.campaign_id)
      if (data) {
        this.campaign = data
      }
      this.SET_LOADING(false)
    },

    handleAddRating(data: any) {
      data["user"] = this.userInfo
      this.campaign.ratings.unshift(data)
    },
    changeTab(tab: string) {
      this.tab = tab
    },
    handleAddTransaction(data: any){
      this.campaign.transactions.unshift(data)
      if (data.type_transaction == 'INCREASE')
        this.campaign.total_budget += data.value
      else this.campaign.used_budget += data.value
    }
  },
  computed: {
    ...mapGetters("user", ["userInfo"]),
    ...mapState(["is_loading"]),
  },
  async created() {
    await this.getCampaignDetail()
  },
  beforeUpdate(){
    document.title = this.campaign.title + ' | V-Volunteer'
    if (this.userInfo?.full_name == this.campaign.user.full_name)
      this.isAuth = true
    else this.isAuth = false
  },
})

export default class CampaignDetail extends Vue {
}

</script>

<style lang="scss" scoped>
.campaign-detail {
  &__section {
    border-radius: 20px;
    font-size: 1rem;
    margin-bottom: 2px;
  }

  &__background {
    background-color: white;
    border-radius: 20px 20px 0 0;
    padding-bottom: 5px;
  }
}

.main-container {
  max-width: 900px;
  margin: 0 auto;
}
</style>