<template>
  <div class="has-background-white p-6">
    <div class="box has-background-light" style="font-size: 1rem">
      <div class="is-flex is-justify-content-space-between">
        <span><strong>Target:</strong> {{ campaign.estimate_budget }}$</span>
        <span>{{ progressDonate }}%</span>
      </div>
      <progress class="progress is-primary" :value="progressDonate" max="100"></progress>
      <div><strong>Total donation:</strong> {{ campaign.total_budget }}$</div>
      <div><strong>Used:</strong> {{ campaign.used_budget }}$</div>
      <div><strong>Remaining:</strong> {{ campaign.total_budget - campaign.used_budget }}$</div>
      <div class="is-flex is-justify-content-space-between mt-4" v-if="campaign.user.id == tokenInfo.user_id">
        <button class="button is-warning is-rounded" @click="open2= true">Add Spent Transaction</button>
        <button v-if="campaign.total_budget < campaign.estimate_budget" class="button is-link is-rounded" @click="open= true">Donate</button>
        <button v-else class="button is-link is-rounded" disabled>This campaign has reached the target</button>
      </div>
      <div class="is-flex is-justify-content-end mt-4" v-else>
        <button v-if="campaign.total_budget < campaign.estimate_budget" class="button is-link is-rounded" @click="open= true">Donate</button>
        <button v-else class="button is-link is-rounded" disabled>This campaign has reached the target</button>
      </div>
    </div>

    <el-table :data="campaign.transactions" stripe size="large" style="width: 100%">
      <el-table-column type="index" width="50"/>
      <el-table-column prop="time" label="Date" min-width="150" sortable/>
      <el-table-column prop="name" label="Name" min-width="200" sortable/>
      <el-table-column prop="description" label="Content" width="250"/>
      <el-table-column prop="value" label="Transactions" min-width="180" align="center">
        <template #default="scope">
          <span class="tag is-primary" v-if="scope.row.type_transaction == 'INCREASE'">
            +{{ scope.row.value }} $
          </span>
          <span class="tag is-danger" v-else>
            -{{ scope.row.value }} $
          </span>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="open" title="Your help will give light to the next generation!">
      <el-form :model="form">
        <el-form-item label="Donation amount" label-width="140px">
          <el-input-number v-model="form.money" min="1"/>
          <span class="ml-2">$</span>
        </el-form-item>
        <el-form-item label="Content" label-width="140px">
          <el-input
            :rows="3"
            type="textarea"
            v-model="form.content"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <button class="button is-primary" @click="sendDonate('INCREASE')">
            Send Donate
          </button>
        </span>
      </template>
    </el-dialog>

    <el-dialog v-model="open2" title="Add spent transaction">
      <el-form :model="form">
        <el-form-item label="Spent amount" label-width="140px">
          <el-input-number v-model="form.money" min="1"/>
          <span class="ml-2">$</span>
        </el-form-item>
        <el-form-item label="Content" label-width="140px">
          <el-input
            :rows="3"
            type="textarea"
            v-model="form.content"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <button class="button is-primary" @click="sendDonate('DECREASE')">
            Add
          </button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapGetters} from "vuex";
import {ActionTypes} from "@/types/store/ActionTypes";
import {ElNotification} from "element-plus";

@Options({
  props: {
    campaign: {
      total_budget: 1,
      estimate_budget: 1,
      used_budget: 0
    } as any
  },
  data() {
    return {
      open: false,
      open2: false,
      form: {
        money: 10,
        content: '',
      },
    }
  },
  methods: {
    ...mapActions('transaction', [ActionTypes.CREATE_TRANSACTION]),

    async sendDonate(type: string) {
      const data = {
        description: this.form.content,
        value: this.form.money,
        event_id: this.campaign.id,
        type_transaction: type
      }

      let res = await this.CREATE_TRANSACTION(data)
      if (res.status == 201) {
        let date: Date = new Date()
        let dateFormat = [date.getDate(), date.getMonth() + 1, date.getFullYear()].join('-')
        const new_data = {
          name: this.userInfo.full_name,
          time: dateFormat,
          type_transaction: type,
          description: this.form.content,
          value: this.form.money,
        }
        this.open = false
        this.open2 = false
        this.$emit('add-transaction', new_data)
        ElNotification({
          message: "You've just donated for this campaign. Thank you!",
          type: "success",
        });
      }
    }
  },
  computed: {
    ...mapGetters("user", ["userInfo"]),
    ...mapGetters("authentication",["tokenInfo"]),
    progressDonate(){
      return Math.floor(this.campaign.total_budget*100 / this.campaign.estimate_budget)
    }
  }
})

export default class DonationSection extends Vue {
}

</script>

<style>

</style>