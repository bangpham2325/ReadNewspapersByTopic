export default interface TokenInfo {
  access_token: string;
  refresh_token: string;
  exp: number;
  iat: number;
  user_id: string;
}