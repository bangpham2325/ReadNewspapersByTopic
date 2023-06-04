<template>
  <el-row class="layout">
    <el-col :span="8">
      <LogoWeb></LogoWeb>
    </el-col>

    <el-col :span="10">
      <el-row>
          <div class="sign is-flex is-justify-content-right" style="width:100%;">
            <input class="input is-rounded mr-4" v-model="searchText" @keyup.enter="searchData" type="text" placeholder="Tìm kiếm" style="height:35px;">  
            <el-button icon="Search" circle @click="searchData"/>

            <el-popover
              placement="bottom"
              trigger="click"
              width="100%"
              v-model:visible="popoverVisible"
            >
              <template #default>
                <div style="margin: 3% 6% 3% 6%;">
                  <div class="tile is-ancestor">
                    <div class="tile is-parent" v-for="(topic, index) in category" :key="index">
                      <el-button type="text" class="subtitle is-6 has-text-centered" style="width: 100%;color:#00773e;" @click="filterByCategory(topic.title, topic.id)">
                        {{ topic.title }}
                      </el-button>
                    </div>
                  </div>

                </div>
              </template>

              <template #reference>
                <el-button icon="Expand" circle/>
              </template>
            </el-popover>
          </div>
      </el-row>  
    </el-col>

    <el-col :span="6">
      <div class="sign is-flex is-justify-content-right" v-if="userInfo.full_name != null">
        <AvatarUser :avatar="userInfo.avatar"></AvatarUser>
      </div>

      <div class="sign is-flex is-justify-content-right" v-else>
        <router-link to="/login">
          <div class="sign__text">Login</div>
        </router-link>
        <router-link to="/register">
          <div class="sign__type button is-light">Sign up</div>
        </router-link>
      </div>
    </el-col>
  </el-row>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {mapActions, mapState, mapGetters, mapMutations} from "vuex";
import {MutationTypes} from "@/types/store/MutationTypes"
import LogoWeb from "@/components/LogoWeb.vue";
import AvatarUser from "@/components/AvatarUser.vue";
import { ActionTypes } from '@/types/store/ActionTypes';

@Options({
  components: {
    AvatarUser,
    LogoWeb
  },

  data(){
    return {
      category: [],
      popoverVisible: false,
      searchText: ""
    }
  },

  methods: {
    ...mapMutations("authentication",[MutationTypes.LOGOUT]),
    ...mapMutations("user",[MutationTypes.CLEAR_USER_INFO]),
    ...mapMutations(["SET_LOADING"]),

    ...mapActions("topic", [ActionTypes.FETCH_TOPICS]),

    async getCategory(){
      this.SET_LOADING(true)
      let data = await this.FETCH_TOPICS()
      if (data) {
        this.category = data.results
      }
      this.SET_LOADING(false)
    },

    searchData(){
      this.$router.push({name: 'searchpage', params: {text: this.searchText}})
      this.searchText = ""
    },

    filterByCategory(topic_name: string, topic_id: string){
      this.$router.push({ name: 'posts-by-category', params: {name:topic_name, id: topic_id } })
      this.popoverVisible = false
    },

  },
  computed: {
    ...mapState(["is_loading"]),
    ...mapGetters("user", ["userInfo"]),
  },
  
  async created() {
    await this.getCategory()
  },
})

export default class TopBar extends Vue {
}


</script>

<style lang="scss" scoped>
@import "@/views/home/style.scss";

.tile.is-ancestor {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 10px;
}
.layout{
  padding: 2% 5% 0% 5%;
  background: white;
}

.sign {
  font-size: 1rem;
  font-weight: 500;
  text-align: center;

  &__type {
    display: inline-block;
    height: 40px;
    width: 100px;
    background-color: #121221;
    border-radius: 60px;
    color: white;
    transition: all 0.2s ease-in-out;
  }

  &__text {
    margin: 0 20px;
    line-height: 40px;
    display: inline-block;
    color: #121221;
    text-transform: capitalize;
    transition: visibility 0.1s, opacity 0.3s linear;
  }
}
</style>