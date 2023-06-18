interface Env {
  IMAGE_URL: string | undefined,
  VALID_TIME: string | undefined,
  BASE_URL: string | undefined,
  BASE_URL_CRAWL: string | undefined,
  API_URL: string | undefined,
  END_MAIL: string | undefined,
  VUE_APP_GOOGLE_CLIENT_ID: string | undefined,
}

export const env: Env = {
  IMAGE_URL: process.env.VUE_APP_IMAGE_URL,
  VALID_TIME: process.env.VUE_APP_VALID_TIME,
  BASE_URL: process.env.VUE_APP_BASE_URL,
  BASE_URL_CRAWL: process.env.VUE_APP_BASE_URL_CRAWL,
  API_URL: process.env.VUE_APP_API_URL,
  END_MAIL: process.env.VUE_APP_END_MAIL,
  VUE_APP_GOOGLE_CLIENT_ID: process.env.VUE_APP_GOOGLE_CLIENT_ID,
};
