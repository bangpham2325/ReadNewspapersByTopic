import { GetterTree } from 'vuex'
import { State } from './state'
import TokenInfo from "@/types/authentication/TokenInfo";

export type Getters = {
  tokenInfo(state: State): TokenInfo
}

export const getters: GetterTree<State, State> & Getters = {
  tokenInfo: (state) => state.tokenInfo
}