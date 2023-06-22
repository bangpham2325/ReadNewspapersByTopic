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
  [ActionTypes.FETCH_POSTS](
    { commit }: AugmentedActionContext,
    params: any
  ): void,
  [ActionTypes.MY_POSTS](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.FETCH_POSTS_BY_AUTHOR](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.FETCH_POST_LIBRARY](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.FETCH_POST_DETAIL](
    { commit }: AugmentedActionContext,
    id: string
  ): void,

  [ActionTypes.FETCH_POST_COMMENT_RATING](
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

  [ActionTypes.FETCH_POST_NEW](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.FETCH_POST_BLOG](
    { commit }: AugmentedActionContext,
    params: any
  ): void,
  [ActionTypes.RECOMENDATION_POST](
    { commit }: AugmentedActionContext,
    id: string
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

  [ActionTypes.UPDATE_STATUS_POST](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.PUBLISH_LIST_POST](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.DELETE_POST](
    { commit }: AugmentedActionContext,
    id: string
  ): void,

  [ActionTypes.ADD_USER_POST](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.UPDATE_USER_POST](
    { commit }: AugmentedActionContext,
    params: any
  ): void,
}

export const actions: ActionTree<State, State> & Actions = {
  async [ActionTypes.FETCH_POSTS]({ commit}, params) {
    let data: any = await PostService.getAllPosts(params)
    return data
  },

  async [ActionTypes.MY_POSTS]({ commit}, params) {
    let data: any = await PostService.getMyPosts(params)
    return data
  },

  async [ActionTypes.FETCH_POSTS_BY_AUTHOR]({ commit}, params) {
    let data: any = await PostService.getPostsByAuthor(params)
    return data
  },

  async [ActionTypes.FETCH_POST_LIBRARY]({ commit }, params) {
    let data: any = await PostService.getPostByLibrary(params)
    return data
  },

  async [ActionTypes.FETCH_POST_DETAIL]({ commit }, slug) {
    let response: any = await PostService.getPostDetail(slug)
    return response
  },

  async [ActionTypes.FETCH_POST_COMMENT_RATING]({ commit }, slug) {
    let response: any = await PostService.getPostCommentRating(slug)
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

  async [ActionTypes.FETCH_POST_NEW]({ commit}, params) {
    let data: any = await PostService.getNewPosts(params)
    return data
  },

  async [ActionTypes.FETCH_POST_BLOG]({ commit}, params) {
    let data: any = await PostService.getBlogPosts(params)
    return data
  },

  async [ActionTypes.RECOMENDATION_POST]({ commit}, id) {
    let data: any = await PostService.recommendPost(id)
    return data
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

  async [ActionTypes.UPDATE_STATUS_POST]({ commit }, data) {
    let response: any = await PostService.updateStatusPost(data.id, data.status)
    return response
  },

  async [ActionTypes.PUBLISH_LIST_POST]({ commit }, params) {
    let response: any = await PostService.publishListPost(params)
    return response
  },

  async [ActionTypes.DELETE_POST]({ commit }, id) {
    let response: any = await PostService.deletePost(id)
    return response
  },

  async [ActionTypes.ADD_USER_POST]({ commit }, params) {
    let response: any = await PostService.addUserPost(params)
    return response
  },

  async [ActionTypes.UPDATE_USER_POST]({ commit }, params) {
    let response: any = await PostService.updateUserPost(params.id, params.data)
    return response
  },
}
