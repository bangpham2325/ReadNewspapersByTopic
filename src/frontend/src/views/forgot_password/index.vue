<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="3"></el-col>
          <el-col :span="12">
            <router-link to="/home">
              <div class="logo is-flex is-justify-content-left">
                <div class="logo__icon">N</div>
                <div class="logo__text">Portal</div>
              </div>
            </router-link>
          </el-col>
        </el-row>
      </el-header>
      <hr>
      <el-main class="columns is-centered">
        <ForgotPasswordPage></ForgotPasswordPage>
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
import {Options, Vue} from "vue-class-component";
import ForgotPasswordPage from "@/views/forgot_password/ForgotForm.vue";

@Options({
  components: {
    ForgotPasswordPage
  },
  mounted() {
    document.title = 'Login to New Portal'
  }
})

export default class ForgotPage extends Vue {}
</script>

<style scoped lang="scss">

</style>
