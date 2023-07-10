<template>
  <div class="chart-section">
    <div class="columns is-flex is-vcentered">
      <div class="column">
        <h3 class="is-size-5 mb-2" style="font-weight: 500">{{title}}</h3>
      </div>
      <div class="column is-flex is-justify-content-end">
        <el-select
          v-if="month"
          v-model="_month"
          class="m-2"
          placeholder="Tháng"
          size="large"
          style="width: 100px"
          @change="$emit('changeMonth', _month)"
        >
          <el-option
            v-for="item in monthOptions"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>

        <el-select
          v-model="_year"
          class="m-2"
          placeholder="Year"
          size="large"
          style="width: 100px"
          @change="$emit('changeYear', _year)"
        >
          <el-option
            v-for="item in yearOptions"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
      </div>
    </div>
    <Bar
      v-if="!month"
      :width="width"
      :height="height"
      :data="{
        labels: ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'],
          datasets: [
            {
              label: 'Admin',
              backgroundColor: '#2196f3',
              borderRadius: '4',
              data: report.total_admin
            },
            {
              label: 'Author',
              backgroundColor: '#008394',
              borderRadius: '4',
              data: report.total_author
            },
            {
              label: 'User',
              backgroundColor: '#ffc107',
              borderRadius: '4',
              data: report.total_user
            },
          ]
      }"
    />
    <div v-if="bar_loading && month" v-loading="bar_loading" class="progress" style="min-height: 100px">
      <div class="progress-bar is-primary is-size-7" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
        Loading...
      </div>
    </div>

    <Bar
    v-if="!bar_loading && month"
    :width="width"
    :height="height"
    :data="dataChart"
    :key="JSON.stringify(dataChart)"
    />
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {Bar} from 'vue-chartjs'
import {Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, Plugin} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

@Options({
  components: {
    Bar
  },
  props: {
    category_report: [],
    report: {},
    year: 2020,
    title: '',
    month: '',
    bar_loading: true
  },
  data() {
    return {
      monthOptions: [1,2,3,4,5,6,7,8,9,10,11,12],
      _month: this.month,
      _year: this.year,
      width: 400,
      height: 100,
      yearOptions: [],
      dataChart: {
        labels: ['Chính Trị Xã Hội', 'Đời Sống', 'Khoa học', 'Kinh doanh', 'Pháp luật', 'Sức khỏe', 'Thế giới', 'Thể thao', 'Văn hóa', 'Vi tính'],
        datasets: [
          {
            label: 'Số bài viết',
            backgroundColor: '#008394',
            borderRadius: '4',
            data: [0,0,0,0,0,0,0,0,0,0]
          },
        ]
      }
    }
  },
  watch: {
    category_report: {
      handler(){
        this.dataChart.datasets[0].data = this.category_report
      },
      deep: true
    }
  },
  created() {
    for (let i = 2023; i <= new Date().getFullYear(); i++) {
      this.yearOptions.push(i)
    }
  }
})
export default class ChartSection extends Vue {
}

</script>

<style scoped>
.chart-section {
  background-color: white;
  border-radius: 20px;
  padding: 40px;
  margin-top: 10px;
}

p {
  font-weight: 600;
  font-size: 18px;
  line-height: 19px;
  color: #797D8C;
}

.date-picker .block:last-child {
  border-right: none;
}
</style>