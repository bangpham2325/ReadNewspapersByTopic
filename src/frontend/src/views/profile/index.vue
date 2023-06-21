<template>
  <router-view></router-view>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import ProfileEdit from "@/views/profile/edit/index.vue";

@Options({
  components: {
    ProfileEdit
  }
})

export default class ProfileBasePage extends Vue {
}
</script>

<style lang="scss" scoped>
  
</style>