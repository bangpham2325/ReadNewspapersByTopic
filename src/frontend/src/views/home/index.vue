<template>
  <div class="common-layout">
    <el-container class="is-flex">
      <el-header>
        <el-row>
          <el-col :span="3"></el-col>
          <el-col :span="12">
            <router-link to="/home">
              <div class="logo is-flex is-justify-content-left">
                <div class="logo__icon">v</div>
                <div class="logo__text">Volunteer</div>
              </div>
            </router-link>
          </el-col>
          <el-col :span="5">
            <div class="sign is-flex is-justify-content-right">
              <router-link to="/login">
                <div class="sign__text">Login</div>
              </router-link>
              <router-link to="/register">
                <div class="sign__type button is-light">Sign up</div>
              </router-link>
            </div>
          </el-col>
        </el-row>
      </el-header>
      <el-main style="margin-top: 60px">
        <el-row>
          <el-col :span="3"></el-col>
          <el-col :span="12">
            <h1 class="title is-1 is-flex">What is Volunteer World?</h1>
            <p style="width: 80%">
              Volunteer World is the world's leading volunteering platform. We
              show you how to volunteer abroad! Search & compare the best
              international volunteer programs offered by volunteer
              organizations and local NGOs with just a few clicks.
            </p>
            <div
              :class="['sign', 'is-flex', 'is-justify-content-left', 'my-5']"
            >
              <router-link to="/register">
                <div class="sign__type button is-light" style="width: 150px">
                  Get started
                </div>
              </router-link>
              <router-link to="/download">
                <div class="sign__text">Download now</div>
              </router-link>
            </div>
          </el-col>
          <el-col :span="5">
            <img style="float: right" src="@/assets/vectors/app.svg" />
            <p style="text-align: center">
              <img
                class="mt-5"
                width="100"
                src="@/assets/images/get-on-google-play.png"
              />
            </p>
          </el-col>
        </el-row>
      </el-main>
      <footer class="footer">
        <div class="content has-text-centered">
          <p>
            <strong>Project</strong> V-Volunteer. The source code is licensed.
          </p>
        </div>
      </footer>
    </el-container>
  </div>
</template>

<script>
export default {
  created() {
    document.title = "Home Page | E-Learning";
  },
};
</script>

<style lang="scss">
@import "@/views/home/style.scss";
</style>
