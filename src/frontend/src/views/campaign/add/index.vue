<template>
 <div class="main-container">
    <TitleBar :title="title"></TitleBar>
	  <div class="create-section has-background-white">
      <AddCampaign :options="options"></AddCampaign>
    </div>
 </div>
</template>

<script lang="ts">
import {Options, Vue} from "vue-class-component";
import AddCampaign from "@/views/campaign/add/AddCampaign.vue";
import TitleBar from "@/components/TitleBar.vue";
import {mapActions, mapMutations} from "vuex";
import {ActionTypes} from "@/types/store/ActionTypes";
import {ElNotification} from "element-plus";
import TopicItem from "@/types/campaign/TopicItem";

@Options({
  components: {
    TitleBar,
    AddCampaign
  },
  data() {
    return {
      title: "Create Your Campaign",
      options: [] as TopicItem[],
    }
  },
  methods: {
    ...mapActions("topic",[ActionTypes.FETCH_TOPICS]),
    ...mapMutations(["SET_LOADING"]),

    async fetchTopics() {
      let data: any = await this.FETCH_TOPICS();

      if (data) {
        this.options = data.results as TopicItem[]
      } else {
        ElNotification({
          title: 'Error',
          message: 'Loading data failed.',
          type: 'error',
        })
      }
    }
  },
  async created(){
    this.SET_LOADING(true)
    await this.fetchTopics()
    setTimeout(() => {
      this.SET_LOADING(false)
    }, 200)
  },
  mounted() {
    document.title = 'Create Your Campaign | V-Volunteer'
  }
})

export default class AddCampaignPage extends Vue {}
</script>

<style lang="scss" scoped>
.main-container {
  max-width: 900px;
  margin: 0 auto;

  .create-section {
    border-radius: 20px;
  }
}
</style>
