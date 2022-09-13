import { state } from "./state";
import { actions } from "./actions";
import { mutations } from "./mutations";
import { getters } from "./getters";
import { Module } from "vuex";

export const campaign: Module<any, any> = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
