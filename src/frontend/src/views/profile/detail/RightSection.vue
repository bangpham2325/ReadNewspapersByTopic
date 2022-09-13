<template>
  <div class="profile-section">
    <h1 class="is-size-5 mb-5">Joined Campaigns</h1>
    <el-row :gutter="12">
      <el-col v-for="item in processList" class="mb-6" :xl="8" :sm="12" :xs="24">
        <router-link v-if="item.status === PROCESS_STATUS.REGISTERED" :to="'/campaigns/' + item.event.id">
          <div class="card">
            <header class="card-header">
              <p class="card-header-title">
                {{ item.event.title }}
              </p>
            </header>
            <div class="card-image">
              <figure class="image is-16by9">
                <img v-if="!item.event.background"
                  src="https://www.fossmint.com/wp-content/uploads/2019/02/Udemy-Python-Learning-Courses-for-Beginners.png" alt="Placeholder image">
                <img v-else :src="item.event.background" alt="Placeholder image">
              </figure>
            </div>
            <div class="card-content">
              <div class="media">
                <div class="media-left">
                  <figure class="image is-48x48">
                    <img v-if="item.event.user.avatar" :src="item.event.user.avatar" alt="Lecturer" class="is-rounded"
                      style="height: 100%">
                    <img v-else src="@/assets/vectors/default_avatar.svg" alt="Lecturer" class="is-rounded"
                      style="height: 100%">
                  </figure>
                </div>
                <div class="media-content">
                  <p class="title is-4 is-capitalized">{{ item.event.user.full_name }}</p>
                  <p class="subtitle is-6">{{ item.event.summary }}</p>
                </div>
              </div>
            </div>
          </div>
        </router-link>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import { PROCESS_STATUS } from '@/const/process_status';
import { ActionTypes } from '@/types/store/ActionTypes';
import { Options, Vue } from 'vue-class-component';
import { mapActions } from 'vuex';

@Options({
  props: {
    user: {},
    processList: {}
  },
  data() {
    return {
      campaignProcess: {} as any,
      activeIndex: "1",
      tab: 'Newsfeed',
      PROCESS_STATUS: PROCESS_STATUS,
    }
  },
})

export default class RightSection extends Vue {
}
</script>

<style lang="scss" scoped>
.card-header-title{
  display: inline-block;
  width: 180px;
  white-space: nowrap;
  overflow: hidden !important;
  text-overflow: ellipsis;
  margin-bottom: 0px;
}
</style>