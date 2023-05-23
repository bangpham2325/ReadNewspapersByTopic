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

@Options({
  components: {
    TopBar
  },
})

export default class BasePage extends Vue {
}
</script>

<style lang="scss" scoped>

</style>