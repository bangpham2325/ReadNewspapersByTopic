import { BaseService } from "@/services/BaseService";
import UserProfile from "@/types/user/UserProfile";

class UserService extends BaseService{
  get entity() {
    return "users"
  }

  async getUserInfo(id: string) {
    try {
      const res: any = await this.request().get(`${this.entity}/${id}/`);
      return res;
    } catch (e) {
      return null;
    }
  }

  async updateUserInfo(id: string, data: UserProfile){
    try {
      const response= await this.request().put(`${this.entity}/${id}/`, data);
      return response;
    } catch (error) {
      return null;
    }
  }

  async updateUserAvatar(data: UserProfile){
    try {
      const response= await this.request().patch(`${this.entity}/update_avatar/`, data);
      return response;
    } catch (error) {
      return null;
    }
  }

}

export default new UserService();