import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import HomePage from '@/views/home/index.vue';
import LoginPage from '@/views/login/index.vue';
import RegisterPage from '@/views/register/index.vue';
import BasePage from "@/views/base/index.vue";
import CampaignBasePage from '@/views/campaign/index.vue';
import DashboardPage from '@/views/campaign/dashboard/index.vue';
import AddCampaignPage from "@/views/campaign/add/index.vue";
import EditCampaignPage from "@/views/campaign/edit/index.vue";
import CampaignManagementPage from "@/views/campaign/management/index.vue";
import TopicBasePage from "@/views/topic/index.vue";
import TopicManagementPage from "@/views/topic/management/index.vue";
import CampaignDetail from "@/views/campaign/detail/index.vue";
import ProfileBasePage from "@/views/profile/index.vue";
import ProfileDetail from "@/views/profile/detail/index.vue";
import ProfileEdit from "@/views/profile/edit/index.vue";
import MyCampaignPage from "@/views/campaign/my/index.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: BasePage,
    children: [
      {
        path: "campaigns",
        name: "campaigns",
        component: CampaignBasePage,
        children: [
          {
            path: "",
            name: "dashboard",
            component: DashboardPage,
          },
          {
            path: "my",
            name: "joined-campaign",
            component: MyCampaignPage,
          },
          {
            path: "add",
            name: "add-campaign",
            component: AddCampaignPage,
          },
          {
            path: ":campaign_id/edit",
            name: "edit-campaign",
            component: EditCampaignPage,
          },
          {
            path: "management",
            name: "campaign-management",
            component: CampaignManagementPage,
          },
          {
            path: ":campaign_id",
            name: "campaign-detail",
            component: CampaignDetail,
          },
        ],
      },
      {
        path: "profile",
        name: "profile",
        component: ProfileBasePage,
        children: [
          {
            path: "",
            name: "profile-detail",
            component: ProfileDetail,
          },
          {
            path: "edit",
            name: "profile-edit",
            component: ProfileEdit,
          },
        ],
      },
      {
        path: "categories",
        name: "categories",
        component: TopicBasePage,
        children: [
          {
            path: "management",
            name: "category-management",
            component: TopicManagementPage,
          },
        ],
      },

  ]
  },
  {
    path: "/home",
    name: "homepage",
    component: HomePage,
  },
  {
    path: "/login",
    name: "login",
    component: LoginPage,
  },
  {
    path: "/logout",
    name: "logout",
    component: BasePage,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterPage,
  },
];
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return {top: 0}
  },
})

export default router
