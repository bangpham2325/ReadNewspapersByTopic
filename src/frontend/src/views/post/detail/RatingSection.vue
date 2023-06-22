<template>
  <div class="rating-section">
    <div v-for="rating in post_rating" :key="rating" class="rating-item">
      <div class="rating-info">
        <div class="avatar">
          <img class="is-rounded" v-if="rating.user.avatar" :src="rating.user.avatar" alt="User Avatar">
          <img v-else src="@/assets/vectors/default_avatar.svg" alt="Default Avatar">
        </div>
        <div class="rating-details">
          <div class="rating-meta">
            <span class="user-name">{{ rating.user.full_name }}</span>
            <span class="date">{{ rating.time_rating }}</span>
          </div>
        </div>
      </div>
      <a-rate class="star-rating" :value="rating.star_rating" />
      <p class="rating-content">{{ rating.title }}</p>
    </div>
  </div>
</template>
  
<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { mapActions, mapGetters, mapState } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElNotification } from "element-plus";
import { ROLES } from "@/const/roles";

@Options({
  props: {
    post_rating: [],
  },
  data() {
    return {
      status: false,
      ROLES: ROLES
    };
  },

  computed: {
    ...mapGetters("user", ["userInfo"]),
    ...mapState("user", ["userInfo"])
  },

  watch: {
    post_rating(newPropValue){
      console.log('Child prop updated:', newPropValue);
    }
  }

})
export default class RatingSection extends Vue {
}
</script>
  
<style scoped>
.rating-section {
  margin-top: 30px;
}

.rating-item {
  background-color: #f9f9f9;
  border: 1px solid #eaeaea;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 20px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.rating-info {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.rating-details {
  margin-left: 10px;
}

.rating-title {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.rating-meta {
  display: flex;
  align-items: center;
}

.user-name {
  font-weight: bold;
  margin-right: 5px;
}

.date {
  font-style: italic;
  color: #666;
}

.star-rating {
  margin-bottom: 10px;
}

.rating-content {
  margin: 0;
  color: #666;
}

@media (max-width: 768px) {
  .rating-item {
    padding: 15px;
  }

  .avatar {
    width: 40px;
    height: 40px;
  }

  .rating-title {
    font-size: 16px;
  }
}
</style>