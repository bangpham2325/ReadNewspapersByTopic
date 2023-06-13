import { ActionTypes } from '@/types/store/ActionTypes'
import { ActionTree, ActionContext } from 'vuex'
import { State } from './state'
import { Mutations } from './mutations'
import { MutationTypes } from '@/types/store/MutationTypes'
import TokenInfo from "@/types/authentication/TokenInfo";
import AuthenticationService from "@/services/authentication/AuthenticationService";
import LoginItem from "@/types/login/LoginItem";
import RegisterItem from "@/types/register/RegisterItem";
import ForgotItem from "@/types/login/Forgot";

type AugmentedActionContext = {
  commit<K extends keyof Mutations>(
    key: K,
    payload: Parameters<Mutations[K]>[1]
  ): ReturnType<Mutations[K]>,

  commit<K extends keyof Mutations>(
    key: K
  ): ReturnType<Mutations[K]>,

} & Omit<ActionContext<State, State>, 'commit'>

export interface Actions {
  [ActionTypes.GET_TOKEN_INFO](
    { commit }: AugmentedActionContext,
    payload: TokenInfo
  ): void,

  [ActionTypes.SET_TOKEN_INFO](
    { commit }: AugmentedActionContext,
    payload: TokenInfo
  ): void,

  [ActionTypes.LOGIN](
    { commit }: AugmentedActionContext,
    payload: LoginItem
  ): any,

  [ActionTypes.LOGIN_WITH_GOOGLE](
    { commit }: AugmentedActionContext,
    payload: LoginItem
  ): any,


  [ActionTypes.REGISTER](
    { commit }: AugmentedActionContext,
    payload: RegisterItem
  ): any,

  [ActionTypes.FORGOT_PASSWORD](
    { commit }: AugmentedActionContext,
    payload: ForgotItem
  ): any,
}

export const actions: ActionTree<State, State> & Actions = {
  [ActionTypes.GET_TOKEN_INFO]({ commit }, payload) {
    if (payload) {
      commit(MutationTypes.GET_TOKEN_INFO, payload);
    }
  },

  [ActionTypes.SET_TOKEN_INFO]({ commit }, payload) {
    if (payload) {
      commit(MutationTypes.SET_TOKEN_INFO, payload);
    }
  },

  async [ActionTypes.LOGIN]({ commit }, payload) {
    const response: any = await AuthenticationService.login(payload)
    if (response.status == 200) {
      commit(MutationTypes.SET_TOKEN_INFO, {
          access_token: response.data.access_token as string,
          refresh_token: response.data.refresh_token as string,
          user_id: response.data.user_id as string
      });
    } 
    return response;
  },

  async [ActionTypes.LOGIN_WITH_GOOGLE]({ commit }, payload) {
    const response: any = await AuthenticationService.login_with_google(payload)
    if (response.status == 200) {
      commit(MutationTypes.SET_TOKEN_INFO, {
          access_token: response.data.access_token as string,
          refresh_token: response.data.refresh_token as string,
          user_id: response.data.user_id as string
      });
    } 
    return response;
  },

  async [ActionTypes.REGISTER]({ commit }, payload) {
    const response: any = await AuthenticationService.register(payload)
    return response;
  },

  async [ActionTypes.FORGOT_PASSWORD]({ commit }, payload) {
    const response: any = await AuthenticationService.forgot_password(payload)
    return response;
  }
}
