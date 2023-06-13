<template>
  <div v-show="!is_loading">
    <title-bar :title="'My Profile'"></title-bar>
    <TopSection :user="user"></TopSection>
    <el-row :gutter="20">
      <el-col :md="8">
        <LeftSection :user="user"></LeftSection>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapMutations, mapGetters, mapState} from "vuex";
import {ActionTypes} from "@/types/store/ActionTypes";
import TopSection from "@/views/profile/detail/TopSection.vue";
import LeftSection from "@/views/profile/detail/LeftSection.vue";
import TitleBar from "@/components/TitleBar.vue";

@Options({
    components: {
      TitleBar,
      TopSection,
      LeftSection
    },
    data() {
      return {
        user: {
          role: "" as String
        } as any,
      }
    },
    methods: {
      ...mapActions('user', [ActionTypes.GET_USER_PROFILE]),
      ...mapMutations(["SET_LOADING"]),
      async getProfileDetail() {
        let response: any = await this.GET_USER_PROFILE(this.tokenInfo.user_id)
        if (response.status == 200) {
          this.user = response.data
        }
      },
    },
    computed: {
      ...mapGetters("authentication", ["tokenInfo"]),
      ...mapState(["is_loading"]),
    },
    async created() {
      this.SET_LOADING(true)
      await this.getProfileDetail()
      this.SET_LOADING(false)
    }
  },
)

export default class ProfileDetail extends Vue {
}
</script>

<style lang="scss" scoped>
.profile-section {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
}
</style>