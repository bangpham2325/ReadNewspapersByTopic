import { ActionTypes } from '@/types/store/ActionTypes'
import { ActionTree, ActionContext } from 'vuex'
import { State } from './state'
import { Mutations } from './mutations'
import RatingService from "@/services/campaign/RatingService";

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
  [ActionTypes.FETCH_RATINGS](
    { commit }: AugmentedActionContext,
    id: string
  ): any,
  [ActionTypes.CREATE_RATING](
    { commit }: AugmentedActionContext,
    payload: any,
  ): any,
}

export const actions: ActionTree<State, State> & Actions = {
  async [ActionTypes.FETCH_RATINGS]({ commit }, id) {
    let data: any = await RatingService.getAll(id)
    return data
  },

  async [ActionTypes.CREATE_RATING]({ commit }, payload) {
    let data: any = await RatingService.create(payload.id, payload.data)
    return data
  },
}
