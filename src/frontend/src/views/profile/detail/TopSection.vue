<template>
  <div class="profile-section">
    <div class="columns is-flex is-vcentered">
      <div class="column is-flex is-justify-content-center is-one-fifth">
        <figure class="image is-128x128 ml-3">
          <img v-if="user.avatar" :src="user.avatar" class="is-rounded" style="height: 100%">
          <img v-else src="@/assets/vectors/default_avatar.svg" class="is-rounded" style="height: 100%"/>
        </figure>
      </div>

      <div class="column">
        <p class="title is-4 is-capitalized">{{ user.full_name }}</p>
        <p class="subtitle is-6 is-italic is-capitalized">{{ user.role.toLowerCase() }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';

@Options({
  props: {
    user: {}
  }
})

export default class TopSection extends Vue {}
</script>