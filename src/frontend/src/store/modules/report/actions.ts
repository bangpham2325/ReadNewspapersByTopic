import { ActionTypes } from '@/types/store/ActionTypes'
import { ActionTree, ActionContext } from 'vuex'
import { State } from './state'
import { Mutations } from './mutations'
import ReportService from "@/services/post/ReportService";

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
  [ActionTypes.FETCH_REPORT_USER](
    { commit }: AugmentedActionContext,
    params: any
  ): void,
  [ActionTypes.FETCH_REPORT_POST](
    { commit }: AugmentedActionContext,
    params: any
  ): void,
}

export const actions: ActionTree<State, State> & Actions = {
  async [ActionTypes.FETCH_REPORT_USER]({ commit}, params) {
    let data: any = await ReportService.reportUser(params)
    return data
  },

  async [ActionTypes.FETCH_REPORT_POST]({ commit}, params) {
    let data: any = await ReportService.reportPost(params)
    return data
  },
}
