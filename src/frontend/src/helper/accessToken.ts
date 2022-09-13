export function accessToken() : string {
  const store = require("../store");
  return store.default.getters["authentication/tokenInfo"].access_token || null;
}

