import decodeToken from "@/utils/decodeToken";
import TokenInfo from "@/types/authentication/TokenInfo";

export function storeTokenToVuex(access_token: string, refresh_token: string, user_id: string): TokenInfo {
  const decoded_token: any = decodeToken(access_token);
  const token = {
    access_token: access_token,
    refresh_token: refresh_token,
    exp: decoded_token.exp,
    iat: decoded_token.iat,
    user_id: user_id
  };
  const store = require("@/store");
  store.default.dispatch("authentication/getTokenInfo", token);
  return token;
}
