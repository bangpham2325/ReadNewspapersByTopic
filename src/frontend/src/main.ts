import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { QuillEditor } from '@vueup/vue-quill'
import * as Sentry from "@sentry/vue";
import { BrowserTracing } from "@sentry/tracing";

import '@vueup/vue-quill/dist/vue-quill.snow.css';
import 'element-plus/dist/index.css'
import "vue-toastification/dist/index.css";

import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
import vue3GoogleLogin from 'vue3-google-login'
library.add(fas, far, fab)

import axios from "axios";
import { env } from "../env";
axios.defaults.baseURL = env.BASE_URL ? env.BASE_URL : "http://127.0.0.1:8000"

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(vue3GoogleLogin, {
  clientId: '284448553155-14qt653a7h2f3233uloeq9tfr2jl76lp.apps.googleusercontent.com'
})
app.use(store).use(router).use(ElementPlus).use(Antd)
app.component('font-awesome-icon', FontAwesomeIcon)
app.component('QuillEditor', QuillEditor)
app.mount('#app')
