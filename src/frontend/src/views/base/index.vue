<template>
  <div class="base">
    <Sidebar :items="items" @collapse="is_collapse = $event"/>
    <div :class="['main', {'main--collapse': is_collapse}]">
      <TopBar :userName="userInfo.full_name" :avatar="userInfo.avatar"></TopBar>
      <div class="container p-4">
        <div class="is-loading-bar has-text-centered" :class="{'is-loading': is_loading }">
          <div class="lds-dual-ring"></div>
        </div>
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapState, mapGetters, mapMutations} from "vuex";
import Sidebar from "@/components/Sidebar.vue";
import TopBar from "@/components/TopBar.vue";
import {ROUTES} from '@/const/routes'
import {ROLES} from "@/const/roles";
import {MutationTypes} from "@/types/store/MutationTypes";
import MenuItem from "@/types/sidebar/MenuItem";

@Options({
  components: {
    Sidebar,
    TopBar
  },
  data() {
    return {
      items: [
        {name: 'campaigns', icon: 'fa-solid fa-signs-post', route: ROUTES.DASHBOARD},
        {name: 'my campaigns', icon: 'fa-solid fa-briefcase', route: ROUTES.CAMPAIGN_MANAGEMENT},
        {name: 'joined', icon: 'fa-solid fa-mattress-pillow', route: ROUTES.MY_CAMPAIGN},
      ] as MenuItem[],
      is_collapse: true
    }
  },
  methods: {
    ...mapMutations("authentication",[MutationTypes.LOGOUT]),
    ...mapMutations("user",[MutationTypes.CLEAR_USER_INFO]),

    goToHome() {
      switch (this.userInfo.role) {
        case ROLES.USER: this.$router.push("/campaigns"); break;
        case ROLES.ADMIN: this.$router.push("/campaigns"); break;
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
    if(!this.userInfo.role)
      this.goToHome()

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
.main {
  height: 100%;
  margin-left: 300px;
  width: calc(100% - 300px);
  z-index: 2;
  transition: all 0.3s;

  &--collapse {
    margin-left: 70px;
    width: calc(100% - 70px);
  }
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