<template>
  <router-link v-if="campaign.title != undefined" :to="'/campaigns/'+campaign.id">
    <div class="campaign-item">

      <div class="campaign-item__title columns">
        <h3 class="column p-0 campaign-item__title__text">{{ campaign.title }}</h3>

        <div class="column is-flex is-justify-content-end p-0 is-one-fifth">
          <el-dropdown size="large">
              <span class="campaign-item__ellipsis el-dropdown-link" @click.prevent="">
                <font-awesome-icon icon="fa-solid fa-ellipsis"/>
              </span>
            <template #dropdown>
              <el-dropdown-menu>
                <router-link :to="'/campaigns/' + campaign.id">
                  <el-dropdown-item icon="View">
                    View detail
                  </el-dropdown-item>
                </router-link>

                <restricted-view :routes="ROUTES.CAMPAIGN_MANAGEMENT.name">
                  <router-link :to="'/campaigns/' + campaign.id + '/edit'">
                    <el-dropdown-item icon="Edit">
                      Edit
                    </el-dropdown-item>
                  </router-link>

                  <el-dropdown-item icon="Delete" @click="dialogVisible = true">
                    Delete
                  </el-dropdown-item>
                </restricted-view>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <div class="campaign-item__summary">
        {{ campaign.summary }}
      </div>

      <div class="campaign-item__info">
        <p class="campaign-item__info__instructor is-flex is-justify-content-space-between">
            <span>
              <font-awesome-icon icon="fa-solid fa-chalkboard-user" class="mr-1"/>
            {{ campaign.user.full_name }}
            </span>
          <span v-if="campaign.avg_rating">
              {{ campaign.avg_rating }} / 5
              <font-awesome-icon icon="fa-solid fa-star" class="ml-1"/>
            </span>
        </p>
      </div>

      <div class="campaign-item__image">
        <img v-if="!campaign.background"
             src="https://www.fossmint.com/wp-content/uploads/2019/02/Udemy-Python-Learning-Courses-for-Beginners.png">
        <img v-else :src="campaign.background">
      </div>
    </div>
  </router-link>

  <router-link v-else to="/campaigns/add">
    <div class="campaign-item is-flex" style="height: calc(100% - 40px); min-height: 300px">
      <div class="button-add">
        <font-awesome-icon icon="fa-solid fa-plus"/>
      </div>
    </div>
  </router-link>

  <restricted-view :routes="[ROUTES.CAMPAIGN_MANAGEMENT.name]">
    <el-dialog
      v-model="dialogVisible"
      title="Delete Campaign"
      width="50%"
      style="border-radius: 20px"
      center>
        <span style="word-break: break-word">
          Are you sure to delete this campaign? This should be undone!
        </span>
      <template #footer>
          <span class="dialog-footer">
            <button class="button is-light is-rounded mr-3" @click="dialogVisible = false">Cancel</button>
            <button class="button is-dark is-rounded" @click="handleDelete">
              Confirm
            </button>
          </span>
      </template>
    </el-dialog>
  </restricted-view>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';

import RestrictedView from "@/components/RestrictedView.vue";
import {ROUTES} from "@/const/routes";
import {ActionTypes} from "@/types/store/ActionTypes";
import {mapActions} from "vuex";
import {ElMessage} from "element-plus";

@Options({
  components: {RestrictedView},
  props: {
    campaign: {} as any,
  },

  data() {
    return {
      dialogVisible: false,
      ROUTES: ROUTES,
      avg_rating: 4.5
    }
  },
  computed: {
    campaign_progress() {
      if (!this.total_lesson || !this.campaign.lessons_completed) return 0
      return Math.round(this.campaign.lessons_completed * 100 / this.total_lesson)
    },
    total_lesson() {
      if (!this.campaign.chapters) return 0
      let result = this.campaign.chapters.reduce(
        (prev: number, curr: any) => {
          return prev + curr.lessons.length
        }, 0
      )
      return result
    }
  },
  emits: ['deleteCampaign'],
  methods: {
    ...mapActions("campaign", [ActionTypes.DELETE_CAMPAIGN]),
    async handleDelete() {
      let response: any = await this.DELETE_CAMPAIGN(this.campaign.id)
      if (response.status == 204) {
        ElMessage({
          message: `Deleted ${this.campaign.title} successfully.`,
          type: 'success',
        })
        this.$emit('delete-campaign')
      } else {
        ElMessage.error('Delete campaign failed.')
      }
      this.dialogVisible = false
    }
  }
})

export default class CampaignItem extends Vue {
}
</script>

<style scoped lang="scss">
.campaign-item {
  background-color: white;
  border-top: 10px solid #024547;
  border-radius: 10px;
  padding: 15px 15px 10px 15px;
  transition: all 0.1s ease-in-out;
  margin-bottom: 40px;
  display: block;

  &__title {
    font-weight: 400;
    margin: 0 10px;

    &__text {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      width: calc(100% - 32px);
    }
  }

  &__ellipsis {
    height: 32px;
    width: 32px;
    border-radius: 20px;
    text-align: center;
    line-height: 32px;
  }

  &__ellipsis:hover {
    background-color: #024547;
    color: white;
  }

  &__summary {
    display: -webkit-box;
    font-size: 0.9rem;
    overflow: hidden;
    text-overflow: ellipsis;
    height: 60px;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    margin: 10px;
    font-weight: 400;
    color: #777;
  }

  &__info {
    color: #ccc;
    font-size: 0.9rem;
    padding: 15px 10px;
    font-weight: 450;
    text-transform: capitalize;
  }

  &__image {
    img {
      box-shadow: rgba(0, 0, 0, 0.04) 0px 3px 5px;
      border-radius: 10px;
      width: 100%;
      aspect-ratio: 16/9;
      object-fit: cover;
      margin-bottom: 6px;
    }
  }

  .button-add {
    display: block;
    font-size: 2rem;
    background-color: #024547;
    color: #fff;
    width: 64px;
    height: 64px;
    text-align: center;
    line-height: 64px;
    border-radius: 60px;
    margin: auto;
  }
}

a {
  color: #024547;
}

.campaign-item:hover {
  cursor: pointer;
  box-shadow: rgba(0, 0, 0, 0.04) 0px 3px 5px;
  border-top: 10px solid #333;
}

</style>

<style scoped>
:deep(.el-dropdown-menu__item:not(.is-disabled):focus) {
  color: #fff;
  background-color: rgba(2, 69, 71, 0.85);
}

.progress-bar .el-progress--line {
  margin-bottom: 10px;
  width: 100%;
}

:deep(.progress-bar .el-progress-bar__inner) {
  margin: 4px;
  height: calc(100% - 8px);
  max-width: calc(100% - 8px);
}

</style>
  