import { ActionTypes } from '@/types/store/ActionTypes'
import { ActionTree, ActionContext } from 'vuex'
import { State } from './state'
import { Mutations } from './mutations'
import DiscussionService from "@/services/post/DiscussionService";

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
  [ActionTypes.CREATE_COMMENT](
    { commit }: AugmentedActionContext,
    data: any
  ): any,

  [ActionTypes.REPLY_COMMENT](
    { commit }: AugmentedActionContext,
    data: any
  ): any,
  
  [ActionTypes.UPDATE_COMMENT](
    { commit }: AugmentedActionContext,
    data: any
  ): any,

  [ActionTypes.REMOVE_COMMENT](
    { commit }: AugmentedActionContext,
    data: any
  ): any,
}

export const actions: ActionTree<State, State> & Actions = {
  async [ActionTypes.CREATE_COMMENT]({ commit }, data) {
    let response: any = await DiscussionService.create(data.id, data.content)
    return response
  },

  async [ActionTypes.REPLY_COMMENT]({ commit }, data) {
    let response: any = await DiscussionService.reply(data.post_id, data.content)
    return response
  },

  async [ActionTypes.UPDATE_COMMENT]({ commit }, data) {
    let response: any = await DiscussionService.update(data.post_id, data.comment_id, data.content)
    return response
  },

  async [ActionTypes.REMOVE_COMMENT]({ commit }, data) {
    let response: any = await DiscussionService.delete(data.post_id, data.comment_id)
    return response
  },
}