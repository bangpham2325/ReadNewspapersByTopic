import { ActionTypes } from '@/types/store/ActionTypes'
import { ActionTree, ActionContext } from 'vuex'
import { State } from './state'
import { Mutations } from './mutations'
import TopicService from "@/services/post/TopicService";

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
  [ActionTypes.FETCH_TOPICS](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.ADD_TOPIC](
    { commit }: AugmentedActionContext,
    payload: any
  ): void,

  [ActionTypes.UPDATE_TOPIC](
    { commit }: AugmentedActionContext,
    payload: any
  ): void,

  [ActionTypes.DELETE_TOPIC](
    { commit }: AugmentedActionContext,
    id: string
  ): void,
}

export const actions: ActionTree<State, State> & Actions = {
  async [ActionTypes.FETCH_TOPICS]({ commit }, params) {
    let data: any = await TopicService.getAll(params)
    return data
  },

  async [ActionTypes.ADD_TOPIC]({ commit }, payload) {
    let response: any = await TopicService.create(payload)
    return response
  },

  async [ActionTypes.UPDATE_TOPIC]({ commit }, payload) {
    let response: any = await TopicService.update(payload)
    return response
  },

  async [ActionTypes.DELETE_TOPIC]({ commit }, id) {
    let response: any = await TopicService.delete(id)
    return response
  },

}
