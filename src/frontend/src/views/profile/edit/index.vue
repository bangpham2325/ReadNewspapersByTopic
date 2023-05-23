<template>
  <AvatarSection 
  :user="user"
  @changeAvatar="user.avatar = $event"
  style="border:1px solid #ccc!important;"></AvatarSection>
  <el-row
    style="background-color: white; border-radius: 10px; border:1px solid #ccc!important;"
    class="p-5 m-3"
  >
    <InfoSection :editForm="editForm"></InfoSection>
  </el-row>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { mapActions, mapMutations, mapGetters } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import AvatarSection from "./AvatarSection.vue";
import InfoSection from "./InfoSection.vue";
import TopBar from "@/components/TopBar.vue";
import LogoWeb from "@/components/LogoWeb.vue";

@Options({
  components: {
    AvatarSection,
    InfoSection,
    TopBar,
    LogoWeb
  },
  data() {
    return {
      user: {
        role: "" as String
      } as any,
      editForm: {
        account: {
          email: "",
        },
      } as any,
      
    };
  },
  methods: {
    ...mapActions("user", [ActionTypes.GET_USER_PROFILE]),
    ...mapMutations(["SET_LOADING"]),
    async getProfileDetail() {
      this.SET_LOADING(true)
      let response: any = await this.GET_USER_PROFILE(this.tokenInfo.user_id);
      if (response.status == 200) {
        this.user = response.data;
        this.editForm = this.user;
      }
      this.SET_LOADING(false);
    },
  },
  computed: {
    ...mapGetters("authentication", ["tokenInfo"]),
  },
  async created() {
    await this.getProfileDetail();
  },
})
export default class ProfileEdit extends Vue {}
</script>

<style lang="scss">
.layout {
  background-color: #e7e7e7;
  padding: 2.5% 10% 1% 10%;
}
</style>