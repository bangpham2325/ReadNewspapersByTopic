<template>
  <div class="pass">
    <h2 class="title">Thay đổi mật khẩu</h2>
    <div class="form">
      <div class="field">
        <label for="currentPassword" class="label">Nhập mật khẩu hiện tại:</label>
        <div class="control">
          <input type="password" id="currentPassword" v-model="currentPassword" class="input" required>
        </div>
      </div>

      <div class="field">
        <label for="newPassword" class="label">Nhập mật khẩu mới:</label>
        <div class="control">
          <input type="password" id="newPassword" v-model="newPassword" class="input" required>
        </div>
      </div>

			<div class="field">
        <label for="newPassword" class="label">Nhập lại mật khẩu mới:</label>
        <div class="control">
          <input type="password" id="newPassword" v-model="confirmPassword" class="input" required>
					<p class="title is-6" style="color:red;" v-if="confirmPassword !== newPassword && confirmPassword">Mật khẩu không trùng</p>
        </div>
      </div>

      <div class="field">
        <div class="control">
          <button type="submit" class="button is-primary" @click="changePassword" :disabled="isDisabled">Cập nhật</button>
        </div>
      </div>
			
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { mapActions, mapState } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElNotification } from 'element-plus';

@Options({
  data() {
    return {
      currentPassword: '',
      newPassword: '',
			confirmPassword: ''
    };
  },
  methods: {
		...mapActions("user", [ActionTypes.UPDATE_USER_PASSWORD]),
    async changePassword(){
			if(!this.currentPassword || !this.newPassword || !this.confirmPassword)
				ElNotification({
					title: 'Lưu ý',
					message: "Vui lòng điền thông tin đầy đủ!",
					type: 'warning',
				})
			else {
				let res: any = await this.UPDATE_USER_PASSWORD({
					old_password: this.currentPassword,
					new_password: this.newPassword
				})

				if(res.status == 200)
					this.$router.push("/logout")
			}
		}
  },

	computed: {
    isDisabled(): boolean {
      return this.newPassword !== this.confirmPassword;
    }
  },
})

export default class ChangePassword extends Vue {}
</script>

<style lang="scss">
.pass {
	margin: 3% 20% 3% 30%;
}
</style>
