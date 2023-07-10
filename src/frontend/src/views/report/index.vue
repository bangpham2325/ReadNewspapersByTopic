<template>
  <el-container class="is-flex">
    <el-header class="has-background-white" style="min-height: 100px;">
      <TopBar></TopBar>
    </el-header>
    <el-main style="background:#F5F5F5; padding: 0 5%" v-loading="loading">
      <div v-show="!is_loading" class="p-3">
        <TotalSection :report="total_report"></TotalSection>
        <ChartSection
          title="Overall User"
          :report="report"
          :year="year"
          @changeYear="year = $event"
        ></ChartSection>

        <ChartSection
          title="Overall Post"
          :year="year"
          :category_report="category_report"
          :month="month"
          @changeYear="year"
          @changeMonth="handleMonth"
          class="mt-5"
          :bar_loading="bar_loading"
        ></ChartSection>

        <div class="list-section">
          <el-tabs>
            <el-tab-pane>
              <template #label>
                <span class="custom-tabs-label">
                  <el-icon size="large"><Histogram/></el-icon>
                  <span>Admin</span>
                </span>
              </template>
              <UserSection
                  :loading="table_loading"
                  :query="user_query"
                  :users="admin_report"
                  :total="total_admin"
                  @changePage="user_query.page = $event"
                ></UserSection>
            </el-tab-pane>

            <el-tab-pane>
              <template #label>
                <span class="custom-tabs-label">
                  <el-icon size="large"><Management/></el-icon>
                  <span>Author</span>
                </span>
              </template>
              <UserSection
                :loading="table_loading"
                :query="user_query"
                :users="author_report"
                :total="total_athour"
                @changePage="user_query.page = $event"
              ></UserSection>
            </el-tab-pane>


              <el-tab-pane>
                <template #label>
              <span class="custom-tabs-label">
                <el-icon size="large"><UserFilled/></el-icon>
                <span>Users</span>
              </span>
                </template>
                <UserSection
                  :loading="table_loading"
                  :query="user_query"
                  :users="user_report"
                  :total="total_user"
                  @changePage="user_query.page = $event"
                ></UserSection>
              </el-tab-pane>
            </el-tabs>
          </div>
      </div>
    </el-main>
    <footer class="footer">
      <div class="has-text-centered">
        <p>
          <strong>Capstone project 2023.</strong> The source code is licensed.
        </p>
      </div>
    </footer>
  </el-container>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component'
import ChartSection from './ChartSection.vue'
import TotalSection from './TotalSection.vue'
import {mapActions} from "vuex"
import {ActionTypes} from "@/types/store/ActionTypes"
import TopBar from "@/components/TopBar.vue";
import UserSection from "@/views/report/UserSection.vue"

@Options({
  components: {
    TopBar,
    TotalSection,
    ChartSection,
    UserSection
  },
  data() {
    return {
      months: ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6", "Tháng 7", "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"],
      year: new Date().getFullYear(),
      month: new Date().getMonth(),
      total_report: {
        total: 0,
        total_user: 0,
        total_admin: 0,
        total_author: 0,
        total_post: 0,
        total_category: 10
      },
      user_data: {} as any,
      report: {} as any,
      admin: [],
      author: [],
      user: [],
      admin_report: [] as any,
      author_report: [] as any,
      user_report: [] as any,
      post_report: [] as any,
      category_report: [0,0,0,0,0,0,0,0,0,0] as any,
      bar_loading: true,
      user_query: {
        page: 1,
        page_size: 12,
        role: "",
        year: new Date().getFullYear()
      },
      table_loading: false,
      loading: true
    }
  },
  methods: {
    ...mapActions("report", [
      ActionTypes.FETCH_REPORT_USER,
      ActionTypes.FETCH_REPORT_POST,
    ]),
    ...mapActions("post", [ActionTypes.FETCH_POSTS]),

    async getPosts() {
      let data = await this.FETCH_POSTS();
      this.total_report.total_post = data.count
    },

    handleData(){
      for (let month of this.months){
        this.admin.push(this.report[month]["ADMIN"])
        this.author.push(this.report[month]["AUTHOR"])
        this.user.push(this.report[month]["USER"])
      }

      this.report = {}
      this.report['total_admin'] = this.admin
      this.report['total_author'] = this.author
      this.report['total_user'] = this.user
    },

    async fetchReportPost() {
      let res = await this.FETCH_REPORT_POST({month: this.month})
      let month = 'Tháng ' + this.month.toString()
      let report_month = res.report[month]
      this.category_report[0] = report_month['Chính Trị Xã Hội']
      this.category_report[1] = report_month['Đời Sống']
      this.category_report[2] = report_month['Khoa học']
      this.category_report[3] = report_month['Kinh doanh']
      this.category_report[4] = report_month['Pháp luật']
      this.category_report[5] = report_month['Sức khỏe']
      this.category_report[6] = report_month['Thế giới']
      this.category_report[7] = report_month['Thể thao']
      this.category_report[8] = report_month['Văn hóa']
      this.category_report[9] = report_month['Vi tính']

      this.post_report = res.posts
      this.bar_loading= false
    },

    async fetchReportUser() {
      this.getPosts()
      let res = await this.FETCH_REPORT_USER()
      this.total_report.total = res.count
      this.report = res.results.report
      this.user_data = res.results.user
      this.handleData()

      res = await this.FETCH_REPORT_USER({role: 'Admin'})
      this.total_report.total_admin = res.count
      this.admin_report = res.results.users

      res = await this.FETCH_REPORT_USER({role: 'Author'})
      this.total_report.total_author = res.count
      this.author_report = res.results.users

      res = await this.FETCH_REPORT_USER({role: 'User'})
      this.total_report.total_user = res.count
      this.user_report = res.results.users
    },

    async handleMonth(data:any){
      this.bar_loading = true
      this.month = data
      await this.fetchReportPost()
    }
  },
  async created() {
    await this.fetchReportUser()
    await this.fetchReportPost()
    this.loading = false
  }
})
export default class ReportPage extends Vue {
}
</script>

<style>
.list-section {
  margin-top: 30px;
  background: #FFFFFF;
  border-radius: 20px;
  padding: 20px 40px;
}

.custom-tabs-label .el-icon {
  vertical-align: middle;
}

.custom-tabs-label span {
  vertical-align: middle;
  margin-left: 4px;
}

.el-main {
  padding: 0;
}
</style>