import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import HomePage from '@/views/home/index.vue';
import LoginPage from '@/views/login/index.vue';
import RegisterPage from '@/views/register/index.vue';
import ForgotPasswordPage from '@/views/forgot_password/index.vue';
import BasePage from "@/views/base/index.vue";
import ProfileBasePage from "@/views/profile/index.vue";
import ProfileEdit from "@/views/profile/edit/index.vue";
import PostBasePage from "@/views/post/index.vue";
import PostDetailPage from  "@/views/post/detail/index.vue";
import PostCategoryPage from "@/views/post/category/index.vue";
import SearchPage from "@/views/post/search/index.vue";
import BookmarkPage from "@/views/post/bookmark/index.vue";
import ManagementPage from "@/views/post/management/index.vue";
import CategoryPage from "@/views/category/index.vue";
import NewPostPage from "@/views/post/new/index.vue";
import BlogPostPage from "@/views/post/blog/index.vue";
import MyPostByAuthor from "@/views/post/mypostbyauthor/index.vue";

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
            path: "management",
            name: "management-post",
            component: ManagementPage,
          },
          {
            path: "my-posts",
            name: "my-posts-management",
            component: ManagementPage,
          },
          {
            path: "my-posts-by-author/:id",
            name: "my-posts-by-author",
            component: MyPostByAuthor,
          },
          {
            path: "detail/:slug",
            name: "detail-post",
            component: PostDetailPage,
          },
          {
            path: ":name",
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
          {
            path: "new-post",
            name: "new-post",
            component: NewPostPage
          },
          {
            path: "blog-post",
            name: "blog-post",
            component: BlogPostPage
          },
        ]
      },
    ]
  },
  {
    path: "/category",
    name: "category",
    component: CategoryPage,
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
  {
    path: "/forgot_password",
    name: "forgot_password",
    component: ForgotPasswordPage,
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
