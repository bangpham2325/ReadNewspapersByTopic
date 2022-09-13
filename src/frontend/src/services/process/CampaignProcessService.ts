import { BaseService } from "@/services/BaseService";

class CampaignProcessService extends BaseService{
  get entity() {
    return "process-create"
  }

  async getAll() {
    try {
      const res = await this.request().get(`${this.entity}/`)
      const course_process = res.data;
      return course_process;
    } catch (error) {
      return [];
    }
  }

  async create(payload: any) {
    try{
      const response: any = await this.request().post(`${this.entity}/`, payload);
      return response;
    }
    catch(error){
      return null;
    }
  }

  async getDetail(id: string) {
    try{
      const res: any = await this.request().get(`events/${id}/${this.entity}/`);
      return res.data;
    }
    catch(error){
      return null;
    }
  }

  async update(id: string, payload: any) {
    try {
        const res: any = await this.request().put(`events/${id}/process-update/`, payload);
    } catch (error) {
        return null
    }
  }

}

export default new CampaignProcessService();