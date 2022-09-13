import {ROLES} from '@/const/roles';

export const ROUTES = {
  DASHBOARD: {
    name: 'campaigns',
    path: '/campaigns',
  },

  MY_CAMPAIGN: {
    name: 'campaigns',
    path: '/campaigns/my',
  },

  CAMPAIGN_MANAGEMENT: {
    name: 'campaign-management',
    path: '/campaigns/management',
  },

  CAMPAIGN_DETAIL: 'campaign-detail',
  EDIT_CAMPAIGN: 'edit-course',

  LESSON_DETAIL: 'lesson-detail',

  TOPICS: '/topics',
  CHAPTERS: '/chapters',
  TOPIC_MANAGEMENT: '/topics/management',

  LOGIN: '/login',
  LOGOUT: '/logout',
  REGISTER: '/register',
}
