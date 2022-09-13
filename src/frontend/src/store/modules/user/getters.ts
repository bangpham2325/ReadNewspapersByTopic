import { GetterTree } from 'vuex'
import { State } from './state'
import UserInfo from "@/types/user/UserInfo";

export type Getters = {
  userInfo(state: State): UserInfo
}

export const getters: GetterTree<State, State> & Getters = {
  userInfo: (state) => state.userInfo
}