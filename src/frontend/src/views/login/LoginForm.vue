<template>
  <el-form
    ref="loginFormRef"
    class="form p-6 is-half"
    :model="loginForm"
    :rules="rules"
  >
    <div class="title" style="color: #024547; font-size: 2rem;">Welcome to V-Volunteer</div>

    <el-form-item prop="email">
      <el-input
        placeholder="Email"
        v-model="loginForm.email"
        size="large"
        :prefix-icon="email_icon"
        @keyup.enter="onLogin($refs.loginFormRef)"
        :disabled="is_freeze"
      />
    </el-form-item>

    <el-form-item prop="password">
      <el-input
        placeholder="Password"
        v-model="loginForm.password"
        size="large"
        type="password"
        :prefix-icon="password_icon"
        class="mt-1"
        @keyup.enter="onLogin($refs.loginFormRef)"
        :disabled="is_freeze"
      />
    </el-form-item>

    <p :class="['subtitle', 'mt-2', 'is-flex', 'is-justify-content-right']" style="font-size: 1rem">Forgot
      password?</p>

    <div class="field">
      <p :class="['control', 'is-flex', 'is-justify-content-center']">
        <el-button class="button is-success is-fullwidth mt-2" @click="onLogin($refs.loginFormRef)" size="large"
                   :disabled="is_freeze">
          Login
        </el-button>
      </p>

      <p class="subtitle mt-3 is-flex is-justify-content-center" style="font-size: 1rem">
        New to V-Volunteer?
        <router-link class="ml-1" to="/register">Sign up!</router-link>
      </p>
    </div>
  </el-form>
</template>

<script lang="ts">
import {Options, Vue} from "vue-class-component";
import type {FormInstance} from 'element-plus'
import {UserFilled, EditPen} from '@element-plus/icons-vue'
import LoginItem from "@/types/login/LoginItem";
import {mapActions, mapState} from "vuex";
import {ActionTypes} from "@/types/store/ActionTypes";
import {ElNotification} from 'element-plus'

@Options({
  data() {
    return {
      loginForm: {
        email: "",
        password: ""
      } as LoginItem,
      email_icon: UserFilled,
      password_icon: EditPen,
      is_freeze: false,
      rules: {
        email: [
          {required: true, message: 'Please input email', trigger: 'blur'},
          {type: 'email', message: 'Please input correct email address', trigger: ['blur', 'change']}
        ],
        password: [
          {required: true, message: 'Please input password', trigger: 'blur'},
          {min: 6, max: 24, message: 'Length should be 6 to 24', trigger: ['blur', 'change']},
        ]
      } as any,
    }
  },
  methods: {
    ...mapActions("authentication", [ActionTypes.LOGIN]),
    ...mapActions("user", [ActionTypes.GET_USER_INFO]),
    async onLogin(formEl: FormInstance | undefined) {
      if (!formEl) return
      await formEl.validate(async (valid, fields) => {
        if (valid) {
          this.is_freeze = true
          const response: any = await this.LOGIN(this.loginForm)

          if (response.status == 200) {
            const user_info: any = await this.GET_USER_INFO(this.tokenInfo.user_id)
            if (user_info.status == 200) {
              this.$router.push("/")
              return
            }
          } else {
            ElNotification({
              title: 'Error',
              message: 'Username/Password is not correct.',
              type: 'error',
            })
          }
        }
      })
      this.is_freeze = false
    }
  },
  computed: {
    ...mapState("authentication", ["tokenInfo"])
  }
})

export default class LoginForm extends Vue {
}
</script>