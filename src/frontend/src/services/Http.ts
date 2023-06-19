import axios, { AxiosInstance } from "axios";
import { env } from '../../env'
import { refreshToken } from "@/helper/refreshToken";
import { getConfigApp } from "@/helper/getConfigApp";
import { accessToken } from "@/helper/accessToken";
import { storeTokenToVuex } from "@/helper/storeTokenToVuex";

export class Http {
  handlerEnabled: boolean
  instance: AxiosInstance

  constructor(status: any) {
    this.handlerEnabled =
      status && status.handlerEnabled ? status.handlerEnabled : false;
    this.instance = axios.create({
      baseURL: env.API_URL ? `${env.BASE_URL}${env.API_URL}` : '/api/v1',
      headers: {
        "Content-type": "application/json",
        "ngrok-skip-browser-warning": "true"
      }
    });

    this.init()
  }

  init() {
    this.instance.interceptors.request.use((request) =>
      this.requestHandler(request)
    );
    this.instance.interceptors.response.use(
      (response) => this.successHandler(response),
      (error) => this.errorHandler(error)
    );
  }

  requestHandler(request: any) {
    const store = require("@/store");
    const tokenInfo = store ? store.default.getters["authentication/tokenInfo"] : null;
    const authenticated = !request.url.startsWith("auth/login");
    if (authenticated && tokenInfo) {
      const { access_token } = tokenInfo;
      if (access_token && access_token.length !== 0) {
        request.headers["Authorization"] = `Bearer ${accessToken()}`;
      }
    }
    return request;
  }

  errorHandler(error: any) {
    if (error?.response?.status === 401) {
      this.renewToken();
    }
    return Promise.reject(error);
  }

  successHandler(response: any) {
    if (this.handlerEnabled) {
      return response;
    }
    return response;
  }

  async renewToken() {
    const token = refreshToken();
    if (token) {
      const data = getConfigApp();
      data.append("refresh_token", token);
      try {
        await this.instance
          .post(`auth/refresh_token`, data)
          .then((response) => {
            if (response?.status === 200) {
              storeTokenToVuex(
                response.data.access_token,
                response.data.refresh_token,
                response.data.user_id
              );
            } else {
              localStorage.removeItem("vuex");
              localStorage.clear();
            }
          });
      } catch (error) {
        return false;
      }
    }
    return false;
  }
}
