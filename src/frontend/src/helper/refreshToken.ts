export function refreshToken() : string {
  const store = require("../store");
  return store.default?.getters["authentication/tokenInfo"]?.refresh_token || undefined;
}
