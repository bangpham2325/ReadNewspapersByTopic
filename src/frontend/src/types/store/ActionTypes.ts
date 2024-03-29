export enum ActionTypes {
  // Authentication
  GET_TOKEN_INFO = "GET_TOKEN_INFO",
  SET_TOKEN_INFO = "SET_TOKEN_INFO",
  LOGIN = "LOGIN",
  REGISTER = "REGISTER",
  FORGOT_PASSWORD = "FORGOT_PASSWORD",
  LOGIN_WITH_GOOGLE = 'LOGIN_WITH_GOOGLE',

  // USER
  GET_USER_INFO = "GET_USER_INFO",
  GET_USER_PROFILE = "GET_USER_PROFILE",
  UPDATE_USER_PROFILE = "UPDATE_USER_PROFILE",
  UPDATE_USER_AVATAR = "UPDATE_USER_AVATAR",
  UPDATE_USER_CATEGORY = "UPDATE_USER_CATEGORY",
  UPDATE_USER_PASSWORD = "UPDATE_USER_PASSWORD",

  // CAMPAIGN
  FETCH_CAMPAIGNS = "FETCH_CAMPAIGNS",
  FETCH_CAMPAIGN_DETAIL = "FETCH_CAMPAIGN_DETAIL",
  FETCH_CAMPAIGN_MANAGEMENT = "FETCH_CAMPAIGN_MANAGEMENT",
  CREATE_CAMPAIGN = "CREATE_CAMPAIGN",
  UPDATE_CAMPAIGN_INFO = "UPDATE_CAMPAIGN_INFO",
  DELETE_CAMPAIGN = "DELETE_CAMPAIGN",

  // CAMPAIGN POST
  CREATE_CAMPAIGN_POST = "CREATE_CAMPAIGN_POST",
  CREATE_CAMPAIGN_POST_COMMENT = "CREATE_CAMPAIGN_POST_COMMENT",

  // TOPIC
  FETCH_TOPICS = "FETCH_TOPICS",
  ADD_TOPIC = "ADD_TOPIC",
  UPDATE_TOPIC = "UPDATE_TOPIC",
  DELETE_TOPIC = "DELETE_TOPIC",

  //RATING
  CREATE_RATING = "CREATE_RATING",
  FETCH_RATINGS = "FETCH_RATINGS",
  //PROCESS
  FETCH_CAMPAIGN_PROCESS_DETAIL = "FETCH_CAMPAIGN_PROCESS_DETAIL",
  UPDATE_CAMPAIGN_PROCESS = "UPDATE_CAMPAIGN_PROCESS",
  FETCH_USER_CAMPAIGNS_PROCESS = "FETCH_USER_CAMPAIGNS_PROCESS",

  //TRANSACTION
  CREATE_TRANSACTION = "CREATE_TRANSACTION",

  //POST
  FETCH_POSTS = "FETCH_POSTS",
  FETCH_POST_LIBRARY = "FETCH_POST_LIBRARY",
  FETCH_POST_DETAIL = "FETCH_POST_DETAIL",
  FETCH_POST_BY_FILTER = "FETCH_POST_BY_FILTER",
  FETCH_POST_BY_BOOKMARK = "FETCH_POST_BY_BOOKMARK",
  FETCH_POST_NEW = "FETCH_POST_NEW",
  FETCH_POST_BLOG = "FETCH_POST_BLOG",
  RECOMENDATION_POST = "RECOMENDATION_POST",
  DELETE_POST = "DELETE_POST", 
  PUBLISH_LIST_POST = 'PUBLISH_LIST_POST',
  UPDATE_STATUS_POST = "UPDATE_STATUS_POST", 
  ADD_POST_BOOKMARK = "ADD_POST_BOOKMARK",
  LIKE_POST = "LIKE_POST",
  RATE_POST = "RATE_POST",
  MY_POSTS = "MY_POSTS",
  FETCH_POSTS_BY_AUTHOR = "FETCH_POSTS_BY_AUTHOR",
  FETCH_POST_COMMENT_RATING = "FETCH_POST_COMMENT_RATING",
  ADD_USER_POST = "ADD_USER_POST",
  UPDATE_USER_POST = "UPDATE_USER_POST",

  //COMMENT
  FETCH_COMMENTS = "FETCH_COMMENTS",
  CREATE_COMMENT= "CREATE_COMMENT",
  REPLY_COMMENT = "REPLY_COMMENT",
  UPDATE_COMMENT = "UPDATE_COMMENT",
  REMOVE_COMMENT = "REMOVE_COMMENT",

  //REPORT
  FETCH_REPORT_USER = "FETCH_REPORT_USER",
  FETCH_REPORT_POST = "FETCH_REPORT_POST"
  
}
