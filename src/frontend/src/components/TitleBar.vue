<template>
  <div class="columns is-flex is-vcentered pl-3 pr-3 mt-3">
    <div class="column is-flex is-justify-content-start is-one-fifth-mobile">
        <button class="button is-text p-0" @click="$router.back()">
          <font-awesome-icon icon="fa-solid fa-arrow-left"/>
        </button>
    </div>
    <div class="column is-flex is-justify-content-end">
      {{ title }}
      <restricted-view :roles="[ROLES.ADMIN]">
        <button class="button is-text p-0 ml-2" style="font-size: 0.8rem"
                @click="$router.push({path: `${$route.params.campaign_id}/edit`})">
          <font-awesome-icon icon="fa-solid fa-pen" />
        </button>
      </restricted-view>
    </div>
	</div>
</template>

<script lang="ts">
import {Options, Vue} from "vue-class-component";
import { mapState } from "vuex";
import { ROLES } from "@/const/roles";
import RestrictedView from "@/components/RestrictedView.vue";
import { ROUTES } from "@/const/routes";

@Options({
  components: {RestrictedView},
  props: {
    title: ""
  },
  data(){
    return {
      ROLES: ROLES,
      ROUTES: ROUTES
    }
  },
  computed: {
    ...mapState("user", ["userInfo"])
  }
})

export default class AddCoursePage extends Vue {
  title!: string
}
</script>