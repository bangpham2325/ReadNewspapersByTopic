<template>
  <el-form ref="forgotFormRef" class="form p-6 is-half" :model="forgotForm" :rules="rules">
    <div class="title" style="color: #121221; font-size: 2rem;">Welcome to N-Portal</div>

    <el-form-item prop="email">
      <el-input placeholder="Email" v-model="forgotForm.email" size="large" :prefix-icon="email_icon"
        @keyup.enter="onForgot($refs.forgotFormRef)" :disabled="is_freeze" />
    </el-form-item>

    <div class="field">
      <p :class="['control', 'is-flex', 'is-justify-content-center']">
        <el-button class="button is-dark is-fullwidth mt-2" @click="onForgot($refs.forgotFormRef)" size="large"
          :disabled="is_freeze">
          Forgot Password
        </el-button>
      </p>

      <p class="subtitle mt-3 is-flex is-justify-content-center" style="font-size: 1rem">
        New to N-Portal?
        <router-link class="ml-1" to="/register">Sign up!</router-link>
      </p>
    </div>
  </el-form>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import type { FormInstance } from 'element-plus'
import { UserFilled, EditPen } from '@element-plus/icons-vue'
import ForgotItem from "@/types/login/Forgot";
import { mapActions, mapState } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElNotification } from 'element-plus'
import axios from 'axios'
declare const gapi: any;

@Options({
  data() {
    return {
      forgotForm: {
        email: ""
      } as ForgotItem,
      email_icon: UserFilled,
      password_icon: EditPen,
      is_freeze: false,
      rules: {
        email: [
          { required: true, message: 'Please input email', trigger: 'blur' },
          { type: 'email', message: 'Please input correct email address', trigger: ['blur', 'change'] }
        ]
      } as any,
    }
  },
  methods: {
    ...mapActions("authentication", [ActionTypes.FORGOT_PASSWORD]),
    async onForgot(formEl: FormInstance | undefined) {
      if (!formEl) return
      await formEl.validate(async (valid) => {
        if (valid) {
          this.is_freeze = true
          const response = await this.FORGOT_PASSWORD(this.forgotForm)

          if (response.status == 200) {
            ElNotification({
              title: 'Forgot successfully',
              message: 'Help me check your email. we have sent your new password',
              type: 'success',
            })
          } else {
            ElNotification({
              title: 'Error',
              message: "Email is occupied!",
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
  },
  mounted() {
    const script = document.createElement('script');
  }
})

export default class ForgotPasswordPage extends Vue {
}
</script>