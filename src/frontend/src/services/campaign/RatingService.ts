import {BaseService} from "@/services/BaseService";

class RatingService extends BaseService {
  get entity() {
    return "ratings"
  }

  async getAll(id: string) {
    try {
      const response: any = await this.request().get(`events/${id}/${this.entity}/`);
      return response.data;
    } catch (error) {
      return [];
    }
  }

  async create(id: string, data: any) {
    try {
      const response: any = await this.request().post(
        `events/${id}/${this.entity}/`,
        data
      );
      return response
    } catch (error) {
      return null;
    }
  }
}

export default new RatingService();