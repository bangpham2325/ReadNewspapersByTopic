import {BaseService} from "@/services/BaseService";

class TransactionService extends BaseService {
  get entity() {
    return "transactions"
  }

  async create(data: any) {
    try {
      const response: any = await this.request().post(
        `${this.entity}/`, data)
      return response
    } catch (error) {
      return null;
    }
  }

}

export default new TransactionService();