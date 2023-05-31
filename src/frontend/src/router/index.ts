import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import HomePage from '@/views/home/index.vue';
import LoginPage from '@/views/login/index.vue';
import RegisterPage from '@/views/register/index.vue';
import BasePage from "@/views/base/index.vue";
import ProfileBasePage from "@/views/profile/index.vue";
import ProfileEdit from "@/views/profile/edit/index.vue";
import PostBasePage from "@/views/post/index.vue";
import PostDetailPage from  "@/views/post/detail/index.vue";
import PostCategoryPage from "@/views/post/category/index.vue";
import SearchPage from "@/views/post/search/index.vue";
import BookmarkPage from "@/views/post/bookmark/index.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: BasePage,
    children: [
      {
        path: "home",
        name: "homepage",
        component: HomePage,
      },
      {
        path: "profile",
        name: "profile",
        component: ProfileBasePage,
        children: [
          {
            path: "edit",
            name: "profile-edit",
            component: ProfileEdit,
          },
        ],
      },
      {
        path: "post",
        name: "post",
        component: PostBasePage,
        children: [
          {
            path: "detail/:id",
            name: "detail-post",
            component: PostDetailPage,
          },
          {
            path: ":name/:id",
            name: "posts-by-category",
            component: PostCategoryPage,
          },
          {
            path: ":text",
            name: "searchpage",
            component: SearchPage,
          },
          {
            path: "saved",
            name: "bookmark",
            component: BookmarkPage,
          },
        ]
      },
    ]
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
