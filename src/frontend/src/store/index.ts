import { createStore } from 'vuex'
import { authentication } from "@/store/modules/authentication";
import { user } from  "@/store/modules/user";
import { campaign } from '@/store/modules/campaign';
import { topic } from '@/store/modules/topic';
import { campaignProcess } from '@/store/modules/campaignProcess';
import { transaction } from './modules/transaction';
import { rating } from './modules/rating';
import { post } from './modules/post';
import { discussion } from './modules/discussion';

import createPersistedState from "vuex-persistedstate";

export default createStore({
  plugins: [createPersistedState()],
  state: {
    is_loading: false
  },
  getters: {
  },
  mutations: {
    SET_LOADING(state, status) {
      state.is_loading = status
    }
  },
  actions: {
  },
  modules: {
    authentication,
    user,
    campaign,
    topic,
    campaignProcess,
    transaction,
    rating,
    post,
    discussion
  }
})
