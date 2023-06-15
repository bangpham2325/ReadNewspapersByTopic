import UserInfo from "../user/UserInfo";
export default interface PostItem {
    id: string,
    title: string,
    summary: string,
    description: string,
    background: string,
    user: UserInfo,
    slug: string,
  }