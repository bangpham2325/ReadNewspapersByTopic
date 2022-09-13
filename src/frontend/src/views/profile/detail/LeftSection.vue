<template>
  <div class="profile-section">
    <h1 class="is-size-5 mb-2">Bio</h1>
    <div class="is-size-6">
      {{ user.bio }}
    </div>
  </div>

  <!-- <div class="profile-section">
    <h1 class="is-size-5 mb-3 mt-2">Certificates</h1>
    <div v-for="item in user.process_courses" :key="item.id" class="mb-5">
      <router-link :to="{ name: 'certification', params: { course_slug: item.course.slug } }">
        <div v-if="item.status == PROCESS_STATUS.COMPLETED" class="certificate mb-5">
          <vue-pdf-embed :source="item.certificate" />
        </div>
      </router-link>
    </div>
  </div> -->
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import VuePdfEmbed from "vue-pdf-embed";
// import {PROCESS_STATUS} from "@/const/process_status";

@Options({
  props: {
    user: {}
  },
  components: {
    VuePdfEmbed
  },
  // data() {
  //   return {
  //     PROCESS_STATUS: PROCESS_STATUS
  //   }
  // }
})

export default class LeftSection extends Vue {
}
</script>

<style lang="scss" scoped>
.profile-section {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 20px;
}
</style>