<template>
    <div class="has-background-white" style="min-height:500px;">
        <div style="display: inline-block; width: 100%;">
            <div style="padding:20px; margin: 0px; float: right;"> {{ campaign.number_user }}
                <span class="icon">
                    <font-awesome-icon icon="users" />
                </span>
            </div>
        </div>
        <div class="columns  is-multiline is-1 is-variable " style="padding:0px 20px">
            <div v-for="user in campaign.list_number_user" class="column is-half">
                <div class="member-card">
                    <div class="media">
                        <div class="media-left">
                            <figure class="image is-48x48 ">
                                <img v-if="user.user.avatar" class="is-rounded" :src="user.user.avatar"
                                    alt="Placeholder image" style="height: 100%;">
                                <img v-else class="is-rounded" src="@/assets/vectors/default_avatar.svg"
                                    alt="Placeholder image">
                            </figure>
                        </div>
                        <div class="media-content" style="align-self: center;">
                            <p class="title is-4" style="font-size: 1rem;">{{ user.user.full_name }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { campaign } from '@/store/modules/campaign';
import { Options, Vue } from 'vue-class-component';

@Options({
    props: {
        campaign: {} as any
    },
})
export default class MemberSection extends Vue {
    // campaign!: any
}
</script>

<style scoped lang="scss">
.member-card {
    border: 1px solid #DFE0E0;
    border-radius: 8px;
    padding: 10px;
}

.image {
    margin: 0px;
}

.title,
.subtitle {
    margin: 0px;
    margin-top: 0px !important;
}

.border-radius-8 {
    border-radius: 8px;
}
</style>