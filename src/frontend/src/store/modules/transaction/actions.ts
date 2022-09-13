import { ActionTypes } from '@/types/store/ActionTypes'
import { ActionTree, ActionContext } from 'vuex'
import { State } from './state'
import { Mutations } from './mutations'
import TransactionService from "@/services/campaign/TransactionService";

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
  [ActionTypes.CREATE_TRANSACTION](
    { commit }: AugmentedActionContext,
    payload: any
  ): any,
}

export const actions: ActionTree<State, State> & Actions = {
  async [ActionTypes.CREATE_TRANSACTION]({ commit }, payload) {
    let data: any = await TransactionService.create(payload)
    return data
  },
}
