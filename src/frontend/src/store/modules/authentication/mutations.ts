import { MutationTypes } from '@/types/store/MutationTypes'
import { MutationTree } from 'vuex'
import { State } from './state'
import TokenInfo from "@/types/authentication/TokenInfo";
import decodeToken from "@/utils/decodeToken";

export type Mutations<S = State> = {
  [MutationTypes.GET_TOKEN_INFO](state: S, payload: TokenInfo): void,
  [MutationTypes.SET_TOKEN_INFO](state: S, {access_token, refresh_token, user_id}: any): void,
  [MutationTypes.LOGOUT](state: S): void,
}


export const mutations: MutationTree<State> & Mutations = {
  [MutationTypes.GET_TOKEN_INFO](state, payload: TokenInfo) {
    state.tokenInfo = payload
  },

  [MutationTypes.SET_TOKEN_INFO](state, {access_token, refresh_token, user_id}) {
    const {exp, iat}: any = decodeToken(access_token);
    const token: TokenInfo = {
      access_token: access_token,
      refresh_token: refresh_token,
      exp: exp,
      iat: iat,
      user_id: user_id,
    }
    state.tokenInfo = {...token} as TokenInfo
  },

  [MutationTypes.LOGOUT](state) {
    state.tokenInfo = {} as TokenInfo
    localStorage.clear();
  },
}
