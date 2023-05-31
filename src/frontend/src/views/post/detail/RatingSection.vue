<template>
    <div class="has-background-white pd-5" style="min-height:500px;">
        <div class="container" style="padding:20px">
            <div v-if="!this.campaign_fetch.status_rating && process.status === PROCESS_STATUS.REGISTERED">
                <div class="is-flex">
                    <p>Click to rating</p>
                    <a-rate @change="starSelected" v-model:value="numberStar" />
                </div>

                <article class="media">
                    <figure class="media-left">
                        <p v-if="this.userInfo.avatar" class="image is-64x64">
                            <img :src="this.userInfo.avatar" class="is-rounded" style="height: 100%;">
                        </p>
                        <p v-else class="image is-64x64">
                            <img src="@/assets/vectors/default_avatar.svg" class="is-rounded" style="height: 100%;">
                        </p>
                    </figure>
                    <div class="media-content">
                        <div class="field">
                            <p class="control">
                                <input class="input mb-2" v-model="title" autosize type="text" placeholder="Title" />
                                <textarea class="textarea" v-model="content" :autosize="{ minRows: 3, maxRows: 5 }"
                                    placeholder="Add a feedback..."></textarea>
                            </p>
                        </div>
                        <nav class="level" style="float: right">
                            <div class="level-left" @click="sendRating">
                                <div class="level-item">
                                    <a class="button is-info is-rounded">Post</a>
                                </div>
                            </div>
                        </nav>
                    </div>
                </article>
            </div>

            <div v-for="rating in this.campaign_fetch.ratings">
                <article class="media  mb-2 mt-2">
                    <figure class="media-left">
                        <p class="image is-64x64 is-rounded">
                            <img class="is-rounded" v-if="rating.user.avatar" :src="rating.user.avatar" style="height: 100%;">
                            <img v-else src="@/assets/vectors/default_avatar.svg">
                        </p>

                    </figure>
                    <div class="media-content">
                        <div class="content">
                            <p style="margin:0; text-align: justify;">
                                <strong>{{ rating.user.full_name }}</strong> <small>{{ new
                                        Date(rating.created_at).toLocaleString()
                                }}</small>
                                <br>
                                <strong>{{ rating.title }}</strong>
                                <a-rate :value="rating.star_rating" style="float: right" />
                                <br>
                                {{ rating.content }}
                            </p>
                        </div>
                    </div>
                </article>
            </div>
        </div>

    </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import { mapActions, mapGetters } from "vuex";
import { ActionTypes } from "@/types/store/ActionTypes";
import { ElNotification } from 'element-plus';
import { campaign } from '@/store/modules/campaign';
import { Content } from 'ant-design-vue/lib/layout/layout';
import { PROCESS_STATUS } from '@/const/process_status';

@Options({
    props: {
        campaign: {} as any
    },
    data() {
        return {
            PROCESS_STATUS: PROCESS_STATUS,
            numberStar: 1,
            title: '',
            content: '',
            ratings:{},
            campaign_fetch:{},
            process : {}
        }
    },
    async created(){
        this.getRating()
        this.getProcess()
    },
    computed: {
        ...mapGetters("user", ["userInfo"]),
    },
    methods: {
        ...mapActions('campaign', [ActionTypes.FETCH_CAMPAIGN_DETAIL]),
        ...mapActions('rating', [ActionTypes.CREATE_RATING]),
        ...mapActions('campaignProcess', [ActionTypes.FETCH_CAMPAIGN_PROCESS_DETAIL]),
        starSelected(star: number) {
            this.numberStar = star
        },
        async getRating() {
            let data = await this.FETCH_CAMPAIGN_DETAIL(this.campaign.id)
            this.campaign_fetch = data
            this.ratings = data.ratings
        },
        async getProcess() {
            let data = await this.FETCH_CAMPAIGN_PROCESS_DETAIL(this.campaign.id)
            this.process = data
        },
        async sendRating() {
            let response = await this.CREATE_RATING({
                id: this.campaign.id,
                data: {
                    title: this.title,
                    content: this.content,
                    star_rating: this.numberStar
                }
            })
            if (response == 201) {
                this.$emit('add-rating', response.data)
                ElNotification({
                    title: "Thank you!",
                    message: "We appreciate you taking the time to give a rating. If you ever need more support, don’t hesitate to get in touch!",
                    type: "success",
                });
                this.campaign_fetch.status_rating = true
            }
            await this.getRating();
        }
    },

})

export default class RatingSection extends Vue {
    // description!: string
}
</script>

<style scoped lang="scss">
ul {
    margin: 0px !important;
}

.ant-rate {
    margin: 0px;
    padding-left: 10px;
}
</style>