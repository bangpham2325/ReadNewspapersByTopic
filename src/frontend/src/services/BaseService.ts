import { Http } from "./Http";

export class BaseService {
  _entity: string

  constructor() {
    if (!this.entity) {
      throw new Error("Child service class not provide entity");
    }
  }

  get entity() {
    return this._entity
  }

  set entity(str: string) {
    this._entity = str
  }

  request(status = { handlerEnabled: true }) {
    let http = new Http(status)
    return http.instance;
  }
}
