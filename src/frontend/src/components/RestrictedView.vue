<template>
  <slot v-if="permissionValidate && routeValidate"></slot>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapGetters } from "vuex";

@Options({
  props: {
    roles: null,
    routes: null
  },
  computed: {
    ...mapGetters("user", ["userInfo"]),
    permissionValidate(){
      if (!this.roles) return true
      return this.roles.indexOf(this.userInfo.role) != -1
    },
    routeValidate(){
      if (this.routes == null) return true
      return this.routes.indexOf(this.$route.name) != -1
    }
  }
})
export default class RestrictedView extends Vue {}
</script>