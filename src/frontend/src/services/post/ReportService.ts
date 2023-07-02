import {BaseService} from "@/services/BaseService";

class ReportService extends BaseService {
  get entity() {
    return "newspaper/post"
  }
  async reportUser(params: any = null){
    try{
      const res = await this.request().get(`users/admin_report_user/`, {
        params,
      })
      return res.data;
    } catch (error){
      return [];
    }
  }

  async reportPost(params: any = null){
    try{
      const res = await this.request().get(`newspaper/post/admin_report_post/`, {
        params,
      })
      return res.data.results;
    } catch (error){
      return [];
    }
  }
}

export default new ReportService();