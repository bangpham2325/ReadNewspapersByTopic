import {BaseService} from "@/services/BaseService";
import qs from 'qs';

class PostService extends BaseService {
  get entity() {
    return "newspaper/post"
  }

  async getAllPosts(params: any = null){
    try{
      const res = await this.request().get(`${this.entity}/management/`, {
        params,
      })
      return res.data;
    } catch (error){
      return [];
    }
  }

  async getMyPosts(params: any = null){
    try{
      const res = await this.request().get(`${this.entity}/my_posts/`, {
        params,
      })
      return res.data;
    } catch (error){
      return [];
    }
  }

  async getPostsByAuthor(params: any = null){
    try{
      console.log(params)
      const res = await this.request().get(`${this.entity}/get_post_by_author/`, {
        params,
      })
      return res.data;
    } catch (error){
      return [];
    }
  }

  async getPostByLibrary(params: any = null) {
    try {
      const response: any = await this.request().get(`${this.entity}/library/`, {
        params,
      });
      return response.data;
    } catch (error) {
      return [];
    }
  }

  async getPostDetail(slug:string){
    try{
      const response: any = await this.request().get(`${this.entity}/${slug}/content/`);
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
      return res
    } catch(error){
      return null
    }
  }

  async updateStatusPost(id:string, status:any){
    try{
      const res:any = await this.request().patch(`${this.entity}/${id}/`, status)
      return res
    }catch(error){
      return null
    }
  }

  async publishListPost(list_id:any){
    try{
      const res:any = await this.request().patch(`${this.entity}/publish_post/`, list_id)
      return res
    }catch(error){
      return null
    }
  }

  async deletePost(id:string){
    try{
      const res:any = await this.request().delete(`${this.entity}/${id}/`)
      return res
    }
    catch(error){
      return null
    }
  }

  async getNewPosts(params: any = null){
    try{
      const res = await this.request().get(`${this.entity}/new_post/`, {
        params,
      });
      return res.data;
    } catch (error){
      return [];
    }
  }

  async getBlogPosts(params: any = null){
    try{
      const res = await this.request().get(`${this.entity}/list_blog/`, {
        params,
      })
      return res.data;
    } catch (error){
      return [];
    }
  }

  async recommendPost(id:string){
    try{
      const res = await this.request().get(`${this.entity}/${id}/recommend/`)
      return res.data
    }catch(error) {
      return [];
    }
  }
}

export default new PostService();