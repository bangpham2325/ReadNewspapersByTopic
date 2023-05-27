from api_base.services import BaseService
from api_post.models import PostVector


class PostVectorService(BaseService):
    @classmethod
    def create_list_post_vector(cls, data, news_objs):
        post_data = []
        for _idx, news in enumerate(news_objs):
            item = {"post": news, "vector": data[_idx]}
            post_data.append(item)
        post_vector_objs = (PostVector(**post_vector) for post_vector in post_data)
        return post_vector_objs
