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

  async getPostByBookmark(params: any = null){
    try{
      const res: any = await this.request().get(`${this.entity}/list_bookmark/`, {
        params,
      });
      return res.data;
    } catch(error) {
      return [];
    }
  }

  async addPostBookmark(id: string){
    try{
      const res: any = await this.request().get(`${this.entity}/${id}/add_bookmark/`)
      return res
    } catch(error) {
      return null;
    }
  }

  async likePost(id:string){
    try{
      const res:any = await this.request().get(`${this.entity}/${id}/like_post/`)
      return res
    } catch(error){
      return null;
    }
  }

  async ratePost(id:string, content:any){
    try {
      const res:any = await this.request().post(`${this.entity}/${id}/ratings/`, content)
    } catch(error){
      return null
    }
  }
}

export default new PostService();