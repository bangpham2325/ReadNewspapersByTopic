from api_base.services import BaseService
from api_post.models import Posts, Contents


class ContentService(BaseService):
    @classmethod
    def create_list_content(cls, data, news_objs):
        content_data = []
        for _idx, news in enumerate(data):
            contents = news.get("content")
            for content in contents:
                item = {
                    "post": news_objs[_idx],
                    "title": content.get("title"),
                    "paragraph": content.get("paragraph"),
                    "description_img": content.get("description_img"),
                    "image": content.get("image"),
                    "index": content.get("order"),
                }
                content_data.append(Contents(**item))
        return content_data
