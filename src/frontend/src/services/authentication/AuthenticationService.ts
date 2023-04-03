import { BaseService } from "@/services/BaseService";
import LoginItem from "@/types/login/LoginItem";
import RegisterItem from "@/types/register/RegisterItem";

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

  async register(data: RegisterItem){
    try {
      let payload = data as any
      const role = data.role
      delete payload['role']
      const response= await this.request().post(`${this.entity}/registers`, payload);
      return response;
    } catch (error) {
      return false;
    }
  }
}

export default new AuthenticationService();