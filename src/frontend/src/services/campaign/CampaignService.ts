import {BaseService} from "@/services/BaseService";

class CampaignService extends BaseService {
  get entity() {
    return "events"
  }

  async getAll(params: any = null) {
    try {
      const res = await this.request().get(`${this.entity}/`, {
        params,
      });
      const courses = res.data;
      return courses;
    } catch (error) {
      return [];
    }
  }

  async getDetail(slug: string) {
    try {
      const res = await this.request().get(`${this.entity}/${slug}/`);
      return res.data;
    } catch (error) {
      return null;
    }
  }

  async get_campaign_management(params: any = null) {
    try {
      const res = await this.request().get(`${this.entity}/management/`, {
        params,
      });
      const courses = res.data;
      return courses;
    } catch (error) {
      return [];
    }
  }

  async getUserProcesses(params: any) {
    try {
      const res = await this.request().get(`/${this.entity}/process-list/`, {
        params
      })
      const course_process = res.data;
      return course_process;
    } catch (error) {
      return [];
    }
  }

  async create(data: any) {
    try {
      const response: any = await this.request().post(`${this.entity}/`, data);
      return response
    } catch (error) {
      return null
    }
  }

  async update(data: any, id: string) {
    try {
      const response: any = await this.request().put(`${this.entity}/${id}/`, data);
      return response
    } catch (error) {
      return null;
    }
  }

  async delete(id: string) {
    try {
      const res = await this.request().delete(`${this.entity}/${id}/`);
      return res;
    } catch (error) {
      return null;
    }
  }

  async create_post(data: any, id: string) {
    try {
      const response: any = await this.request().post(`${this.entity}/${id}/post-event/`, data);
      return response
    } catch (error) {
      return null
    }
  }

  async create_post_comment(data: any) {
    try {
      const response: any = await this.request().post(`${this.entity}/${data.event_id}/post-event/${data.post_id}/comments/`, data.comment);
      return response
    } catch (error) {
      return null
    }
  }
}

export default new CampaignService();
