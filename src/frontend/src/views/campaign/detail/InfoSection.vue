<template>
  <div class="campaign-detail__section no-lr-top-border has-background-white p-3 columns">

      <div class="column is-half">
        <h1 class="is-size-5 is-capitalized">{{ campaign.title }}</h1>
        <el-row>
          <span v-for="index in 5" 
          :key="index"
          style="color: #eee"
          >
            <font-awesome-icon icon="fa-solid fa-star" :class="{checked:campaign.avg_rating>=index}"/>
          </span>
          <p class="ml-4">{{campaign.avg_rating}}/5 ({{campaign.total_rating}} rating)</p>
        </el-row>

        <p>
          <br>{{ campaign.summary }}
        </p>

        <button
          v-if="(status == PROCESS_STATUS.REGISTERED)"
          class="button is-dark mt-3 is-rounded"
          @click="unRegister">
          Unregister
        </button>

        <button
          v-else
          class="button is-dark mt-3 is-rounded"
          @click="register">
          Register now
        </button>

        <!-- <el-button 
        v-if="course.process_status != PROCESS_STATUS.NOT_OPEN && course.status_rating == false" 
        round size="large"
        class="mx-3 mt-3"
        @click="visible = true">Rating</el-button> -->
      </div>

      <div class="column">
        <h1 class="is-size-5 ml-3 mb-3">Campaign owner</h1>
        <div class="columns">

          <div class="column is-one-third">
            <figure class="image is-128x128">
              <img v-if="campaign.user?.avatar" class="is-rounded" :src="campaign.user?.avatar" style="height: 100%;">
              <img v-else class="is-rounded" src="@/assets/vectors/default_avatar.svg">
            </figure>
          </div>

          <div class="column">
            <h3 class="is-capitalized">{{ campaign.user?.full_name }}</h3>
            <p class="mt-1">{{ campaign.user?.bio }}</p>
          </div>

        </div>
      </div>

      <el-dialog v-model="visible" class="p-5" width="420px" style="border-radius:30px;">
        <template #header>
          <div class="rate" style="width:46px;background-color:#EEEEEE;border-radius: 50%;">
            <label title="text" style="color:#fb7413" class="ml-2">5 stars</label>
          </div>
        </template>
        
        <div class="mt-6">
          <h1 class="title is-3">How did we do?</h1>
          <p class="subtitle is-6 mt-2" style="color:#797D8C;">
            Please let us know how we did with your support request. All feedback is appreciated to help us improve our offering!
          </p>

          <el-row>
            <el-button 
            v-for="i in 5" 
            :key="i"
            @click="starSelected(i)" 
            class="number-star"
            :class="{active: numberStar === i}">{{ i }}</el-button>
          </el-row>

          <el-input
            class="mt-5"
            v-model="title"
            autosize
            type="textarea"
            placeholder="Title"
          />
          <div style="margin: 10px 0" />
          <el-input
            v-model="content"
            :autosize="{ minRows: 3, maxRows: 5 }"
            type="textarea"
            placeholder="Write your feedback"
          />

          <el-button size="large" color="#fb7413" 
          round 
          style="width:100%;color:white" 
          class="mt-5"
          @click="sendRating">Submit</el-button>
        </div>
      </el-dialog>
    </div>

</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { PROCESS_STATUS } from "@/const/process_status";
import { ElNotification } from "element-plus";
import { mapActions } from "vuex";
import {ActionTypes} from "@/types/store/ActionTypes";
import { campaign } from '@/store/modules/campaign';

@Options({
  props: {
    campaign: {} as any
  },
  data() {
    return {
      PROCESS_STATUS: PROCESS_STATUS,
      visible: false,
      title: '',
      content: '',
      numberStar: 0,
      status: ''
    }
  },
  methods: {
    ...mapActions('rating', [ActionTypes.CREATE_RATING]),
    ...mapActions('campaignProcess', [ActionTypes.UPDATE_CAMPAIGN_PROCESS, ActionTypes.FETCH_CAMPAIGN_PROCESS_DETAIL]),

    async getProcessDetail() {
      let data = await this.FETCH_CAMPAIGN_PROCESS_DETAIL(this.$route.params.campaign_id)
      if (data) {
        this.status = data.status
        this.$emit('updateStatus', this.status)
      }
    },

    async register() {
      await this.UPDATE_CAMPAIGN_PROCESS({
        id: this.campaign.id,
        status: {status: 'REGISTERED'}
      })
      
      ElNotification({
        message: "You've just registered for this campaign. Thank you!",
        type: "info",
      });

      this.status = 'REGISTERED'
      this.$emit('updateStatus', this.status)
    },

    async unRegister() {
      await this.UPDATE_CAMPAIGN_PROCESS({
        id: this.campaign.id,
        status: {status: 'UNREGISTER'}
      })
      
      ElNotification({
        message: "You've just unregistered for this campaign.",
        type: "info",
      });

      this.status = 'UNREGISTER'
      this.$emit('updateStatus', this.status)
    },
    starSelected(star: number){
      this.numberStar = star
    },
    async sendRating(){
      let response = await this.CREATE_RATING({
        id: this.course.id,
        data: {
          title: this.title,
          content: this.content,
          star_rating: this.numberStar
        }
      })
      if(response.status == 201){
        this.$emit('add-rating', response.data)
        this.visible = false
        ElNotification({
          title: "Thank you!",
          message: "We appreciate you taking the time to give a rating. If you ever need more support, don’t hesitate to get in touch!",
          type: "success",
        });
      }
    }
  },
  async created(){
    await this.getProcessDetail()
  }
})

export default class InfoSection extends Vue {
  course!: any
}
</script>

<style scoped lang="scss">
.no-lr-top-border {
  border-radius: 0 0 20px 20px !important;
}

.rate {
  float: left;
  height: 46px;

}
.rate:not(:checked) > label {
  float:left;
  width:1em;
  overflow:hidden;
  white-space:nowrap;
  cursor:pointer;
  font-size:30px;
  color:#ccc;
}
.rate:not(:checked) > label:before {
  content: '★ ';
}

.number-star{
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 6px;
  cursor: pointer;
}
.number-star:focus {
  background: #fb7413; 
  color: white;
}
.active {
  background: #fb7413; 
  color: white;
}
.checked {
  color: orange;
}

</style>