import {BaseService} from "@/services/BaseService";

class PostService extends BaseService {
  get entity() {
    return "newspaper/post"
  }

  async getPostByLibrary(params: any = null) {
    try {
      const response: any = await this.request().get(`${this.entity}/library/`);
      return response.data;
    } catch (error) {
      return [];
    }
  }

  async getPostDetail(id:string){
    try{
      const response: any = await this.request().get(`${this.entity}/${id}/`);
      return response.data;
    } catch(error) {
      return null;
    }
  }

  async getPostByFiter(params: any = null){
    try {
      const res: any = await this.request().get(`${this.entity}/`, {
        params,
      });
      return res.data;
    } catch(error) {
      return [];
    }
  }
}

export default new PostService();