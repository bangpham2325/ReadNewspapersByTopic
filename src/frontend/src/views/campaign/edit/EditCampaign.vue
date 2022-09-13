<template>
  <CoverImage
    :image="image"
    :is_freeze="is_freeze"
    @changeImage="this.image = $event"
    @changeFile="this.background = $event"
  >
  </CoverImage>

  <div class="p-6">
    <el-form
      ref="formRef"
      label-position="top"
      label-width="100px"
      :model="campaign"
      size="large"
      :disabled="is_freeze"
      :rules="rules"
    >

      <div class="is-flex is-justify-content-end">
        <span :class="['tag', 'mb-5', {
          'is-black': campaign.status == CAMPAIGN_STATUS.DRAFT,
          'is-primary': campaign.status == CAMPAIGN_STATUS.PUBLISHED,
          'is-danger': campaign.status == CAMPAIGN_STATUS.DEACTIVATED
        }]">
          {{ campaign.status }}
        </span>
      </div>

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
        <button
          class="button is-success is-rounded"
          @click.prevent="handleSubmit($refs.formRef)"
          :disabled="is_freeze">
          <el-icon v-if="is_freeze" class="is-loading mr-2">
            <Loading/>
          </el-icon>
          Save
        </button>
        <div>
          <button
            class="button is-success is-light is-rounded mr-2"
            v-if="campaign.status == CAMPAIGN_STATUS.DRAFT"
            @click.prevent="handlePublish">
            Publish
          </button>
          <button
            class="button is-link is-light is-rounded mr-2"
            v-if="campaign.status == CAMPAIGN_STATUS.PUBLISHED"
            @click.prevent="handleUnpublish">
            Unpublish
          </button>
          <button
            class="button is-danger is-rounded"
            @click.prevent="dialogVisible = true">
            <font-awesome-icon icon="fa-solid fa-trash"/>
          </button>
        </div>
      </div>
    </el-form>
  </div>

  <el-dialog
    v-model="dialogVisible"
    title="Delete Campaign"
    width="50%"
    style="border-radius: 20px"
    center>
    <template #footer>
      <span class="dialog-footer">
        <button class="button is-light is-rounded mr-3" @click="dialogVisible = false">Cancel</button>
        <button class="button is-dark is-rounded" @click="handleDelete">
          Confirm
        </button>
      </span>
    </template>
  </el-dialog>

</template>

<script lang="ts">
import {Options, Vue} from "vue-class-component";
import TopicItem from "@/types/campaign/TopicItem";
import TextEditor from "@/components/TextEditor.vue"
import {ElMessage, ElNotification, FormInstance} from "element-plus";
import {CAMPAIGN_STATUS} from "@/const/campaign_status";
import {mapActions} from "vuex";
import {ActionTypes} from "@/types/store/ActionTypes";
import CoverImage from "@/components/CoverImage.vue";

@Options({
  components: {
    CoverImage,
    TextEditor
  },
  props: {
    options: null,
    campaign: {
      status: CAMPAIGN_STATUS.DRAFT
    }
  },
  data() {
    return {
      CAMPAIGN_STATUS: CAMPAIGN_STATUS,
      dialogVisible: false,
      background: null,
      image: "",
      is_freeze: false,
      expandEditor: false,
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
    }
  },
  methods: {
    ...mapActions("campaign", [ActionTypes.UPDATE_CAMPAIGN_INFO, ActionTypes.DELETE_CAMPAIGN]),
    async handleSubmit(formEl: FormInstance | undefined) {
      if (!formEl) return

      await formEl.validate(async (valid, fields) => {
        if (valid) {
          this.is_freeze = true
          let formData = new FormData();

          formData.append("title", this.campaign.title);
          formData.append("summary", this.campaign.summary);
          formData.append("estimate_budget", this.campaign.estimate_budget);
          formData.append("description", this.campaign.description);
          formData.append("status", this.campaign.status);
          if (this.background != null)
            formData.append("background", this.background?.raw)

          this.campaign.type_events.map((type_event_id: string) => {
            formData.append("type_event_ids", type_event_id)
          })

          const response: any = await this.UPDATE_CAMPAIGN_INFO({
            form: formData,
            id: this.campaign.id
          })

          if (response.status == 201) {
            this.$router.push({
              name: "campaign-detail",
              params: {campaign_id: response.data.id},
            });

            ElNotification({
              title: 'Update successfully',
              message: 'Campaign info has been updated!',
              type: 'success',
            })
          } else {
            ElNotification({
              title: 'Error',
              message: 'Update campaign failed!',
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

    async handleDelete() {
      this.is_freeze = true
      let response: any = await this.DELETE_CAMPAIGN(this.campaign.id)
      if (response.status == 204) {
        this.$router.push('/')
        ElMessage({
          message: `Deleted ${this.campaign.title} successfully.`,
          type: 'success',
        })
        this.$emit('delete-campaign')
      } else {
        ElMessage.error('Delete campaign failed.')
      }
      this.dialogVisible = false
      this.is_freeze = false
    },

    async handlePublish() {
      this.is_freeze = true
      let formData = new FormData()
      formData.append("title", this.campaign.title);
      formData.append("summary", this.campaign.summary);
      formData.append("status", CAMPAIGN_STATUS.PUBLISHED);
      this.campaign.type_events.map((type_event_id: string) => {
        formData.append("type_events_ids", type_event_id ? type_event_id : "")
      })

      const response: any = await this.UPDATE_CAMPAIGN_INFO({
        form: formData,
        id: this.campaign.id
      })

      if (response.status == 201) {
        this.campaign.status = CAMPAIGN_STATUS.PUBLISHED

        ElNotification({
          title: 'Update successfully',
          message: 'Campaign has been published!',
          type: 'success',
        })
      } else {
        ElNotification({
          title: 'Error',
          message: 'Update campaign status failed!',
          type: 'error',
        })
      }

      this.is_freeze = false
    },

    async handleUnpublish() {
      this.is_freeze = true
      let formData = new FormData()
      formData.append("title", this.campaign.title);
      formData.append("summary", this.campaign.summary);
      formData.append("status", CAMPAIGN_STATUS.DRAFT);
      this.campaign.type_events.map((type_event_id: string) => {
        formData.append("type_events_ids", type_event_id ? type_event_id : "")
      })

      const response: any = await this.UPDATE_CAMPAIGN_INFO({
        form: formData,
        id: this.campaign.id
      })

      if (response.status == 201) {
        this.campaign.status = CAMPAIGN_STATUS.DRAFT

        ElNotification({
          title: 'Update successfully',
          message: 'Campaign status has been change to draft!',
          type: 'success',
        })
      } else {
        ElNotification({
          title: 'Error',
          message: 'Update campaign status failed!',
          type: 'error',
        })
      }

      this.is_freeze = false
    }
  },
  created() {
    this.unwatchCampaign = this.$watch('campaign', (newVal: any) => {
      if (newVal) {
        this.image = newVal.background
        this.unwatchCampaign();
      }
    });

    this.CAMPAIGN_STATUS = CAMPAIGN_STATUS
  }
})

export default class CampaignSection extends Vue {
  options!: TopicItem[];
  campaign!: any
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
