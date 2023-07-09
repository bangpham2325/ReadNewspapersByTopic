<template>
    <el-container class="is-flex has-background-white">
      <el-header>
        <el-affix>
          <TopBar></TopBar>
        </el-affix>
      </el-header>
      <el-main :class="component2Class">
      <div class="common-layout">
        <!-- <div class="is-loading-bar has-text-centered" :class="{ 'is-loading': is_loading }">
          <div class="lds-dual-ring"></div>
        </div> -->
        <router-view></router-view>
      </div>
    </el-main>
      <footer class="footer">
        <div class="has-text-centered">
          <p>
            <strong>Capstone project 2023.</strong> The source code is licensed.
          </p>
        </div>
      </footer>
    </el-container>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import TopBar from "@/components/TopBar.vue";
import { mapState, mapGetters, mapMutations } from "vuex";
import { MutationTypes } from "@/types/store/MutationTypes";
import { ROLES } from "@/const/roles";

@Options({
  components: {
    TopBar
  },
  methods: {
    ...mapMutations("authentication", [MutationTypes.LOGOUT]),
    ...mapMutations("user", [MutationTypes.CLEAR_USER_INFO]),

    goToHome() {
      switch (this.userInfo.role) {
        case ROLES.ADMIN: this.$router.push("/post/management"); break;
        case ROLES.AUTHOR: this.$router.push("post/my-posts"); break;
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
    component2Class() {
      if (this.$route.name === 'blog-post') {
        return 'blog-personal';
      } else {
        return '';
      }
    },
  },
  beforeUpdate() {
    switch (this.$route.name) {
      case 'home': this.goToHome(); break;
      case 'logout': this.logout(); break;
    }
  },
  async created() {
    switch (this.$route.name) {
      case 'home': this.goToHome(); break;
      case 'logout': this.logout(); break;
    }
  }
})

export default class BasePage extends Vue {
}
</script>

<style lang="scss" scoped>

.blog-personal {
  background-image: url('https://res.cloudinary.com/ddrpryfpq/image/upload/v1686509761/evgeni-evgeniev-LPKk3wtkC-g-unsplash_plsmyo.jpg');
  background-size: cover;
  background-repeat: no-repeat;
}

:deep(.el-main){
  padding: auto;
}

.blog-personal .common-layout {
  width: 70%;
}

.is-loading-bar {
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}

.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}

@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>