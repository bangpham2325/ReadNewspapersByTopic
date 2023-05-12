from api_base.services import BaseService
from api_post.models import Keyword


class KeywordService(BaseService):
    @classmethod
    def create_list_keyword(cls, data, news_objs):
        keyword_data = []
        for _idx, news in enumerate(data):
            keywords = news.get("keyword")
            for keyword in keywords:
                item = {"post": news_objs[_idx], "keyword": keyword}
                keyword_data.append(item)
        keyword_objs = (Keyword(**keyword) for keyword in keyword_data)
        return keyword_objs
