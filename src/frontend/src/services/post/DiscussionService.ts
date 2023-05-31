import { BaseService } from "@/services/BaseService";

class DiscussionService extends BaseService{
    get entity() {
        return "newspaper/post"
      }

  async create(id: string, content:any) {
    const data = {content: content}
    const response: any = await this.request().post(`${this.entity}/${id}/comments/`, data);
    return response;
  }

  async reply(post_id: string, content: any) {
    const response: any = await this.request().post(`${this.entity}/${post_id}/comments/`, content);
    return response;
  }

  async update(post_id: string, comment_id:string, content:any) {
    const response: any = await this.request().put(`${this.entity}/${post_id}/comments/${comment_id}/`, content);
    return response;
  }

  async delete(post_id: string, comment_id:string) {
    const response = await this.request().delete(`${this.entity}/${post_id}/comments/${comment_id}/`);
    return response;
  }
}

export default new DiscussionService();