<template>
  <router-view v-show="!is_loading"></router-view>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapState} from "vuex";

@Options({
  computed: {
    ...mapState(["is_loading"])
  }
})

export default class PostBasePage extends Vue {
}
</script>

<style lang="scss" scoped>

</style>