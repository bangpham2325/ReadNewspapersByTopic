import { ActionTypes } from '@/types/store/ActionTypes'
import { ActionTree, ActionContext } from 'vuex'
import { State } from './state'
import { Mutations } from './mutations'
import CampaignService from "@/services/campaign/CampaignService";

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
  [ActionTypes.FETCH_CAMPAIGNS](
    { commit }: AugmentedActionContext,
    params: any
  ): void,

  [ActionTypes.FETCH_CAMPAIGN_MANAGEMENT](
    { commit }: AugmentedActionContext,
    params: any
  ): void,
  [ActionTypes.FETCH_CAMPAIGN_DETAIL](
    { commit }: AugmentedActionContext,
    slug: string
  ): any,
  [ActionTypes.CREATE_CAMPAIGN](
    { commit }: AugmentedActionContext,
    formData: FormData
  ): any,
  [ActionTypes.CREATE_CAMPAIGN_POST_COMMENT](
    { commit }: AugmentedActionContext,
    payload: any
  ): any,
  [ActionTypes.UPDATE_CAMPAIGN_INFO](
    { commit }: AugmentedActionContext,
    data: any,
  ): any,
  [ActionTypes.DELETE_CAMPAIGN](
    { commit }: AugmentedActionContext,
    id: string
  ): any,
  [ActionTypes.FETCH_USER_CAMPAIGNS_PROCESS](
    { commit }: AugmentedActionContext,
    id: string
  ): any,
  [ActionTypes.CREATE_CAMPAIGN_POST](
    { commit }: AugmentedActionContext,
    payload: any,
  ): any
}

export const actions: ActionTree<State, State> & Actions = {
  async [ActionTypes.FETCH_CAMPAIGNS]({ commit }, params) {
    let data: any = await CampaignService.getAll(params)
    return data
  },

  async [ActionTypes.FETCH_CAMPAIGN_MANAGEMENT]({ commit }, params) {
    let data: any = await CampaignService.get_campaign_management(params)
    return data
  },

  async [ActionTypes.FETCH_CAMPAIGN_DETAIL]({ commit }, slug) {
    let data: any = await CampaignService.getDetail(slug)
    return data
  },

  async [ActionTypes.CREATE_CAMPAIGN]({ commit }, formData) {
    let data: any = await CampaignService.create(formData)
    return data
  },

  async [ActionTypes.CREATE_CAMPAIGN_POST_COMMENT]({ commit }, payload) {
    let data: any = await CampaignService.create_post_comment(payload)
    return data
  },

  async [ActionTypes.UPDATE_CAMPAIGN_INFO]({ commit }, payload) {
    let data: any = await CampaignService.update(payload.form, payload.id)
    return data
  },

  async [ActionTypes.DELETE_CAMPAIGN]({ commit }, id) {
    let response: any = await CampaignService.delete(id)
    return response
  },
  async [ActionTypes.FETCH_USER_CAMPAIGNS_PROCESS]({ commit }, id) {
    let data: any = await CampaignService.getUserProcesses(id);
    return data;
  },

  async [ActionTypes.CREATE_CAMPAIGN_POST]({ commit }, payload) {
    let data: any = await CampaignService.create_post(payload.form, payload.id)
    return data
  },
}
