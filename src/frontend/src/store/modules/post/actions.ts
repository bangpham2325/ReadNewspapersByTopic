import { ActionTypes } from '@/types/store/ActionTypes'
import { ActionTree, ActionContext } from 'vuex'
import { State } from './state'
import { Mutations } from './mutations'
import PostService from "@/services/post/PostService";

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
  [ActionTypes.FETCH_POST_LIBRARY](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.FETCH_POST_DETAIL](
    { commit }: AugmentedActionContext,
    id: string
  ): void,

  [ActionTypes.FETCH_POST_BY_FILTER](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.FETCH_POST_BY_BOOKMARK](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.ADD_POST_BOOKMARK](
    { commit }: AugmentedActionContext,
    id: string
  ): void,

  [ActionTypes.LIKE_POST](
    { commit }: AugmentedActionContext,
    id: string
  ): any,

  [ActionTypes.RATE_POST](
    { commit }: AugmentedActionContext,
    data: any
  ): any,
}

export const actions: ActionTree<State, State> & Actions = {
  async [ActionTypes.FETCH_POST_LIBRARY]({ commit }, params) {
    let data: any = await PostService.getPostByLibrary(params)
    return data
  },

  async [ActionTypes.FETCH_POST_DETAIL]({ commit }, id) {
    let response: any = await PostService.getPostDetail(id)
    return response
  },

  async [ActionTypes.FETCH_POST_BY_FILTER]({ commit }, params) {
    let response: any = await PostService.getPostByFiter(params)
    return response
  },

  async [ActionTypes.FETCH_POST_BY_BOOKMARK]({ commit }, params) {
    let response: any = await PostService.getPostByBookmark(params)
    return response
  },

  async [ActionTypes.ADD_POST_BOOKMARK]({ commit }, id) {
    let response: any = await PostService.addPostBookmark(id)
    return response
  },

  async [ActionTypes.LIKE_POST]({ commit }, id) {
    let response: any = await PostService.likePost(id)
    return response
  },

  async [ActionTypes.RATE_POST]({ commit }, data) {
    let response: any = await PostService.ratePost(data.id, data.feedback)
    return response
  },
}
