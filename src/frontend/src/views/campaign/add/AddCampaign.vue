<template>
  <CoverImage
    :image="image"
    :is_freeze="is_freeze"
    @changeImage="this.image = $event"
    @changeFile="this.background = $event"
  >
  </CoverImage>

  <el-form
    ref="formRef"
    label-position="top"
    label-width="100px"
    :model="campaign"
    size="large"
    class="p-6"
    :disabled="is_freeze"
    :rules="rules"
  >

    <el-form-item prop="title">
      <span class="title is-5">Title</span>
      <el-input v-model="campaign.title" placeholder="Enter campaign title"/>
    </el-form-item>

    <el-form-item prop="type_events">
      <span class="title is-5 mt-3">Category</span>
      <el-select
        v-model="campaign.type_events"
        multiple
        filterable
        default-first-option
        :reserve-keyword="false"
        style="width: 100%"
        placeholder="Select category for your campaign"
      >
        <el-option
          v-for="item in options"
          :key="item.id"
          :label="item.name"
          :value="item.id"
        />
      </el-select>
    </el-form-item>

    <el-form-item prop="estimate_budget">
      <span class="title is-5 mt-3" style="width: 100%">Estimate budget</span>
      <el-input-number v-model="campaign.estimate_budget" :precision="2" :step="0.1" :min="1"/>
    </el-form-item>

    <el-form-item prop="summary">
      <span class="title is-5 mt-3">Short description</span>
      <el-input v-model="campaign.summary" type="textarea" placeholder="Tell something about this campaign..."/>
    </el-form-item>

    <span class="title is-5 mt-3">
      Description
      <button class="button is-light ml-2" style="font-size: 0.6rem" @click.prevent="expandEditor = true">
        <font-awesome-icon icon="fa-solid fa-up-right-and-down-left-from-center" class="mr-1"/> Expand
      </button>
    </span>
    <div :class="['mt-4', {expandEditor: expandEditor}]">
      <div :class="{expandEditor__content: expandEditor}">
        <TextEditor
          ref="editor"
          :is_freeze="is_freeze"
          :init_content="campaign.description"
          @contentChange="campaign.description = $event"
        />
        <div class="is-flex is-justify-content-center">
          <button v-show="expandEditor" class="button is-rounded" @click.prevent="expandEditor = false">Close</button>
        </div>
      </div>
    </div>
    <div class="is-flex is-justify-content-space-between">
      <div>
        <button
          class="button is-success is-rounded"
          @click.prevent="handleSubmit($refs.formRef, CAMPAIGN_STATUS.PUBLISHED)"
          :disabled="is_freeze">
          <el-icon v-if="is_freeze" class="is-loading mr-2">
            <Loading/>
          </el-icon>
          Save
        </button>
        <button
          class="button is-primary is-rounded ml-2"
          @click.prevent="handleSubmit($refs.formRef, CAMPAIGN_STATUS.DRAFT)"
          :disabled="is_freeze">
          <el-icon v-if="is_freeze" class="is-loading mr-2">
            <Loading/>
          </el-icon>
          Save as draft
        </button>
      </div>
      <button
        class="button is-dark is-rounded"
        @click.prevent="resetForm($refs.formRef)"
        :disabled="is_freeze">
        Reset
      </button>
    </div>
  </el-form>
</template>

<script lang="ts">
import {Options, Vue} from "vue-class-component";
import TopicItem from "@/types/campaign/TopicItem";
import TextEditor from "@/components/TextEditor.vue"
import {ElNotification, FormInstance} from "element-plus";
import {CAMPAIGN_STATUS} from "@/const/campaign_status";
import {mapGetters, mapActions} from "vuex";
import {ActionTypes} from "@/types/store/ActionTypes";
import CoverImage from "@/components/CoverImage.vue";
import {database, ref, push, onValue} from "@/firebase";

@Options({
  components: {
    TextEditor,
    CoverImage
  },
  props: {
    options: [] as TopicItem[],
  },
  data() {
    return {
      CAMPAIGN_STATUS: CAMPAIGN_STATUS,
      campaign: {
        title: "",
        summary: "",
        description: "",
        background: null,
        type_events: [],
        estimate_budget: 1000
      },
      image: "",
      showUpload: true,
      background: null,
      is_freeze: false,
      rules: {
        title: [
          {required: true, message: 'Please input title', trigger: 'blur'},
          {min: 5, max: 100, message: 'Length should be 5 to 100', trigger: 'blur'},
        ],
        type_events: [
          {
            type: 'array',
            required: true,
            message: "Please select at least one campaign category",
            trigger: "blur",
          },
        ],
        summary: [
          {required: true, message: 'Please input summary for this campaign', trigger: 'blur'},
          {min: 20, max: 200, message: 'Length should be 20 to 200', trigger: 'blur'},
        ]
      } as any,
      expandEditor: false
    }
  },
  methods: {
    ...mapActions("campaign", [ActionTypes.CREATE_CAMPAIGN]),
    async handleSubmit(formEl: FormInstance | undefined, status: string) {
      if (!formEl) return
      await formEl.validate(async (valid, fields) => {
        this.is_freeze = true

        if (valid) {
          if (this.background == null) {
            ElNotification({
              title: 'Missing background',
              message: 'Please choose background for your campaign!',
              type: 'warning',
            })
            this.is_freeze = false
            return
          }

          let formData = new FormData();

          let roomid = Array.from({length: 16}, () => "0123456789ABCDEF".charAt(Math.floor(Math.random() * 16))).join('');
          formData.append("title", this.campaign.title);
          formData.append("summary", this.campaign.summary);
          formData.append("description", this.campaign.description);
          formData.append("estimate_budget", this.campaign.estimate_budget);
          formData.append("status", status);
          formData.append("background", this.background?.raw)
          formData.append("user_id", this.tokenInfo.user_id);
          formData.append("room_id", roomid);
          this.campaign.type_events.map((type_event_id: string) => {
            formData.append("type_event_ids", type_event_id)
          })

          const response: any = await this.CREATE_CAMPAIGN(formData)
          push(ref(database, "chatrooms/"), {
            room_id: roomid,
            room_name: this.campaign.title,
          });
          if (response.status == 201) {
            push(ref(database, "chatrooms/"), {
              room_id: roomid,
              room_name: this.campaign.title,
            });
            this.$router.push({
              name: "campaign-detail",
              params: {campaign_id: response.data.id},
            });

            ElNotification({
              title: 'Create campaign successfully',
              message: 'Edit your campaign detail and publish for everyone now!',
              type: 'success',
            })
          } else {
            ElNotification({
              title: 'Error',
              message: 'Create campaign failed!',
              type: 'error',
            })
          }
        } else {
          ElNotification({
            title: 'Missing info',
            message: 'Please fill in all required field!',
            type: 'warning',
          })
        }
        this.is_freeze = false
      })
    },
    resetForm(formEl: FormInstance | undefined) {
      if (!formEl) return
      formEl.resetFields()
    }
  },
  computed: {
    ...mapGetters("authentication", ["tokenInfo"])
  },
  created() {
    this.unwatchCampaign = this.$watch('campaign', (newVal: any) => {
      if (newVal) {
        this.image = newVal.background
        this.unwatchCampaign();
      }
    });
  }
})

export default class AddCampaignPage extends Vue {
  options!: TopicItem[]
}
</script>

<style lang="scss" scoped>
.expandEditor {
  position: fixed;
  top: -20px;
  left: 0;
  right: 0;
  bottom: 0;
  margin: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1999;
  transition: 0.3s all linear;

  &__content {
    position: fixed;
    top: 50%;
    left: 50%;
    z-index: 2000;
    padding: 20px;
    width: 90%;
    background-color: white;
    transform: translate(-50%, -50%);
    border-radius: 20px;
  }
}
</style>