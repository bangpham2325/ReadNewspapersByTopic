import { BaseService } from "@/services/BaseService";
import LoginItem from "@/types/login/LoginItem";
import RegisterItem from "@/types/register/RegisterItem";
import ForgotItem from "@/types/login/Forgot";

class AuthenticationService extends BaseService{
  get entity() {
    return "auth"
  }

  async login(data: LoginItem) {
    try {
      const response: any = await this.request().post(`${this.entity}/login/`, data);
      return response;
    } catch (error) {
      return false;
    }
  }

  async login_with_google(data: any) {
    try {
      const response: any = await this.request().post(`${this.entity}/google/`, data);
      return response;
    } catch (error) {
      return false;
    }
  }

  async register(data: RegisterItem){
    try {
      let payload = data as any
      const role = data.role
      delete payload['role']
      if(role == 'user'){
        const response= await this.request().post(`${this.entity}/registers`, payload);
        return response;
      }
      else {
        const response= await this.request().post(`${this.entity}/registers/author`, payload);
        return response;
      }
    } catch (error) {
      return false;
    }
  }

  async forgot_password(data: ForgotItem){
    try {
      let payload = data as ForgotItem
      const response= await this.request().post(`${this.entity}/forgot-password/`, payload);
      return response;
    } catch (error) {
      return false;
    }
  }
}

export default new AuthenticationService();