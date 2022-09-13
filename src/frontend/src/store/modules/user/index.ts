import { state } from "./state";
import { actions } from "./actions";
import { mutations } from "./mutations";
import { getters } from "./getters";
import { Module } from "vuex";

export const user: Module<any, any> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
