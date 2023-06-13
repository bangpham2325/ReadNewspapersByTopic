import { ActionTypes } from '@/types/store/ActionTypes'
import { ActionTree, ActionContext } from 'vuex'
import { State } from './state'
import { Mutations } from './mutations'
import UserService from "@/services/user/UserService";
import {MutationTypes} from "@/types/store/MutationTypes";
import UserInfo from "@/types/user/UserInfo";

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
  [ActionTypes.GET_USER_INFO](
    { commit }: AugmentedActionContext,
    user_id: string
  ): void,

  [ActionTypes.GET_USER_PROFILE](
    { commit }: AugmentedActionContext,
    user_id: string
  ): any,

  [ActionTypes.UPDATE_USER_PROFILE](
    { commit }: AugmentedActionContext,
    payload: any,
  ): any,

  [ActionTypes.UPDATE_USER_AVATAR](
    { commit }: AugmentedActionContext,
    payload: any,
  ): any,

  [ActionTypes.UPDATE_USER_CATEGORY](
    { commit }: AugmentedActionContext,
    params: any
  ): void,
}

export const actions: ActionTree<State, State> & Actions = {
  async [ActionTypes.GET_USER_INFO]({ commit }, user_id) {
    let response: any = await UserService.getUserInfo(user_id)
    if (response?.status == 200) {
      let user: UserInfo = {
        id: response.data.id,
        full_name: response.data.full_name,
        role: response.data.role,
        avatar: response.data.avatar,
        bio: response.data.avatar,
        email: response.data.account.email,
        categories: response.data.categories
      }
      commit(MutationTypes.SET_USER_INFO, user);
    }
    return response
  },

  async [ActionTypes.GET_USER_PROFILE]({ commit }, user_id) {
    let response: any = await UserService.getUserInfo(user_id)
    return response
  },

  async [ActionTypes.UPDATE_USER_PROFILE]({ commit }, payload) {
    let response: any = await UserService.updateUserInfo(payload.user_id, payload.data)
    return response
  },

  async [ActionTypes.UPDATE_USER_AVATAR]({ commit }, payload) {
    let response: any = await UserService.updateUserAvatar(payload.data)
    return response
  },

  async [ActionTypes.UPDATE_USER_CATEGORY]({ commit }, params) {
    let response: any = await UserService.updateUserCategory(params)
    return response
  },
}


