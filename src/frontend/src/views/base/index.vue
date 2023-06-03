<template>
  <div class="common-layout">
    <el-container class="is-flex">
      <el-header>
        <TopBar></TopBar>
      </el-header>
      <el-main style="margin-top: 20px">
        <router-view></router-view>
      </el-main>
      <footer class="footer">
        <div class="has-text-centered">
          <p>
            <strong>Capstone project 2023.</strong> The source code is licensed.
          </p>
        </div>
      </footer>
    </el-container>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import TopBar from "@/components/TopBar.vue";
import {mapState, mapGetters, mapMutations} from "vuex";
import {MutationTypes} from "@/types/store/MutationTypes";
import {ROLES} from "@/const/roles";

@Options({
  components: {
    TopBar
  },
  methods: {
    ...mapMutations("authentication",[MutationTypes.LOGOUT]),
    ...mapMutations("user",[MutationTypes.CLEAR_USER_INFO]),

    goToHome() {
      switch (this.userInfo.role) {
        case ROLES.ADMIN: this.$router.push("/post/management"); break;
        default: this.$router.push("/home"); break;
      }
    },

    logout() {
      this.LOGOUT()
      this.CLEAR_USER_INFO()
      this.goToHome()
    }
  },
  computed: {
    ...mapState(["is_loading"]),
    ...mapGetters("user", ["userInfo"]),
  },
  beforeUpdate() {
    switch (this.$route.name){
      case 'home': this.goToHome(); break;
      case 'logout': this.logout(); break;
    }
  },
  async created() {
    switch (this.$route.name){
      case 'home': this.goToHome(); break;
      case 'logout': this.logout(); break;
    }
  }
})

export default class BasePage extends Vue {
}
</script>

<style lang="scss" scoped>

</style>