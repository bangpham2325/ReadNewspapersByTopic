<template>
  <el-form
    ref="registerFormRef"
    class="form p-6 is-half"
    :model="registerForm"
    style="min-height: 520px"
    :rules="rules"
  >
    <div class="title" style="color: #121221; font-size: 2rem;">Become a member</div>

    <el-form-item prop="full_name">
      <el-input
        placeholder="Full name"
        v-model="registerForm.full_name"
        size="large"
        prefix-icon="UserFilled"
        :disabled="is_freeze"
      />
    </el-form-item>

    <el-form-item prop="email">
      <el-input
        placeholder="Email"
        v-model="registerForm.email"
        size="large"
        prefix-icon="Message"
        :disabled="is_freeze"
      />
    </el-form-item>

    <el-form-item prop="password">
      <el-input
        placeholder="Password"
        v-model="registerForm.password"
        size="large"
        type="password"
        prefix-icon="EditPen"
        :disabled="is_freeze"
      />
    </el-form-item>

    <el-form-item prop="confirmPassword">
      <el-input
        placeholder="Confirm password"
        v-model="confirmPassword"
        size="large" type="password"
        prefix-icon="EditPen"
        :disabled="is_freeze"
      />
    </el-form-item>

    <el-row>
      <label class="checkbox my-3" style="font-size: 1rem">
        <input type="checkbox" v-model="is_agree_term">
        I agree to the <a href="#"><strong>terms and conditions</strong></a>
      </label>
    </el-row>
    <div class="field">
      <p :class="['control', 'is-flex', 'is-justify-content-center']">
        <el-button
          class="button is-dark is-fullwidth mt-2"
          @click="onRegister($refs.registerFormRef)"
          size="large"
          :disabled="is_freeze"
        >
          Sign up
        </el-button>
      </p>
      <p class="subtitle mt-3 is-flex is-justify-content-center" style="font-size: 1rem">
        Already have an account?
        <router-link to="/login" class="ml-1">Log in</router-link>
      </p>
    </div>
  </el-form>
</template>

<script lang="ts">
import {Options, Vue} from "vue-class-component";
import RegisterItem from "@/types/register/RegisterItem";
import {mapActions} from "vuex";
import {ActionTypes} from "@/types/store/ActionTypes";
import {ElNotification, FormInstance} from 'element-plus'

@Options({
  data() {
    return {
      registerForm: {
        full_name: "",
        email: "",
        password: "",
        role: "user",
      } as RegisterItem,
      confirmPassword: "",
      is_agree_term: false,
      is_freeze: false,
      rules: {
        full_name: [
          {required: true, message: 'Please input full name', trigger: 'blur'},
          {min: 5, max: 30, message: 'Length should be 5 to 30', trigger: ['blur']},
        ],
        email: [
          {required: true, message: 'Please input email', trigger: 'blur'},
          {type: 'email', message: 'Please input correct email address', trigger: ['blur', 'change']}
        ],
        password: [
          {required: true, message: 'Please input password', trigger: 'blur'},
          {min: 6, max: 24, message: 'Length should be 6 to 24', trigger: ['blur']},
        ]
      } as any,
    }
  },
  methods: {
    ...mapActions("authentication", [ActionTypes.REGISTER]),
    async onRegister(formEl: FormInstance | undefined) {
      if (this.confirmPassword != this.registerForm.password) {
        ElNotification({
          title: 'Notice',
          message: 'Please input the correct confirm password!',
          type: 'info',
        })
        return
      }

      if (!this.is_agree_term) {
        ElNotification({
          title: 'Notice',
          message: 'Please read and agree with terms and conditions before sign up!',
          type: 'info',
        })
        return
      }

      if (!formEl) return

      await formEl.validate(async (valid) => {
        let temp = this.registerForm.role
        if (valid) {
          this.is_freeze = true
          const response = await this.REGISTER(this.registerForm)

          if (response.status == 201) {
            ElNotification({
              title: 'Register successfully',
              message: 'You already become a member of E-learning. Please login to enter the world of knowledge.',
              type: 'success',
            })
            this.$router.push("/login");
          } else {
            ElNotification({
              title: 'Error',
              message: "Email is occupied!",
              type: 'error',
            })
          }
        }
        this.registerForm.role = temp
      })
      this.is_freeze = false
    },

  },
})

export default class RegisterForm extends Vue {
}
</script>

<style lang="scss">
:root {
  --card-line-height: 1.2em;
  --card-padding: 0.75em;
  --card-radius: 0.5em;
  --color-green: #07B464;
  --color-gray: #e2ebf6;
  --color-dark-gray: #c4d1e1;
  --radio-border-width: 2px;
  --radio-size: 1.5em;
}

.flex {
  display: flex;
  grid-gap: 1.5em;
  margin: 0 auto;
  max-width: 60em;
  padding: 0;

  @media (min-width: 42em) {
    grid-template-columns: repeat(3, 1fr);
  }
}

.card {
  background-color: #fff;
  border-radius: var(--card-radius);
  position: relative;

  &:hover {
    box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.15);
  }
}

.radio {
  margin: 0;
  position: absolute;
  right: calc(var(--card-padding) + var(--radio-border-width));
  top: calc(var(--card-padding) + var(--radio-border-width));
}

@supports (-webkit-appearance: none) or (-moz-appearance: none) {
  .radio {
    -webkit-appearance: none;
    -moz-appearance: none;
    background: #fff;
    border: var(--radio-border-width) solid var(--color-gray);
    border-radius: 50%;
    cursor: pointer;
    height: var(--radio-size);
    outline: none;
    transition: background 0.2s ease-out,
    border-color 0.2s ease-out;
    width: var(--radio-size);

    &::after {
      border: var(--radio-border-width) solid #fff;
      border-top: 0;
      border-left: 0;
      content: '';
      display: block;
      height: 0.75rem;
      left: 25%;
      position: absolute;
      top: 50%;
      transform: rotate(45deg) translate(-50%, -50%);
      width: 0.375rem;
    }

    &:checked {
      background: var(--color-green);
      border-color: var(--color-green);
    }
  }

  .card:hover .radio {
    border-color: var(--color-dark-gray);

    &:checked {
      border-color: var(--color-green);
    }
  }
}

.content {
  border: var(--radio-border-width) solid var(--color-gray);
  border-radius: var(--card-radius);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  padding: var(--card-padding);
  transition: border-color 0.2s ease-out;
}

.card:hover .content {
  border-color: var(--color-dark-gray);
}

.radio:checked ~ .content {
  border-color: var(--color-green);
}

.radio:focus ~ .content {
  box-shadow: 0 0 0 0.5px var(--color-dark-gray);
}

.radio:disabled ~ .content {
  color: var(--color-dark-gray);
  cursor: default;
}

.radio:disabled ~ .content {
  color: var(--color-dark-gray);
}

.card:hover .radio:disabled ~ .content {
  border-color: var(--color-gray);
  box-shadow: none;
}

.card:hover .radio:disabled {
  border-color: var(--color-gray);
}
</style>