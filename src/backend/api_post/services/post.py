from datetime import datetime
from django.db.models import Q
from django.utils.text import slugify
from api_base.services import BaseService
from django.db.models.functions import Lower
from api_post.constants import PostStatus
from api_post.models import Posts, Category, Source
from api_user.constants import Roles


class PostService(BaseService):
    @classmethod
    def create_post(cls, data):
        categories = data.pop('category')
        post_obj = Posts(**data)
        post_obj.slug = slugify(f"{post_obj.title} {post_obj.id.hex[:5]}")
        post_obj.save()
        post_obj.category.set(categories) if categories else None
        return post_obj

    @classmethod
    def create_list_news(cls, arr_posts, topic):
        category = Category.objects
        in_db_sources = Source.objects.values_list("domain", flat=True)
        source_crawl = list(
            filter(lambda x: x.get("source") not in in_db_sources, arr_posts)
        )
        objs = []
        sources = []
        if source_crawl:
            for index, post in enumerate(source_crawl):
                source = Source(title=post.get("title"), domain=post.get("source"))
                sources.append(source)
                objs.append(Posts(
                    title=post.get("title"),
                    thumbnail=post.get("thumbnail"),
                    category=category.filter(title=topic[index]).first(),
                    source=source,
                    author=post.get("author"),
                    summary=post.get("excerpt"),
                ))
        return source_crawl, objs, sources

    @classmethod
    def get_list_post_by_category(cls, params=None):
        ft = Q(status=PostStatus.PUBLISHED.value)

        if params.get('q'):
            ft &= Q(title_lower__contains=str(params.get('q')).strip().lower())

        posts = Posts.objects.annotate(title_lower=Lower('title')).filter(ft)

        if params.getlist('categories[]'):
            topic_ids = params.getlist('categories[]')
            posts = posts.filter(category__id__in=topic_ids)
        return posts

    @classmethod
    def get_list_post(cls, params=None):
        ft = dict()
        ft.update({'status': PostStatus.PUBLISHED.value})
        if params.get('title'):
            ft.update({'title__contains': params.get('title')})
        if params.get('author'):
            ft.update({'author': params.get('author')})
        if params.get('category_ids'):
            ft.update({'category__id__in': params.getlist('category_ids')})
        if params.get('start_date') and params.get('end_date'):
            ft.update({'publish_date__range': (params.get('start_date', params.get('end_date')))})

        posts = Posts.objects.filter(**ft)

        return posts

    @classmethod
    def get_post_management(cls, params=None):
        ft = Q()
        if params.get('title'):
            ft &= Q(title__contains=params.get('title'))
        if params.get('author'):
            ft &= Q(author=params.get('author'))
        if params.get('category_ids'):
            ft &= Q(category__id__in=params.getlist('category_ids'))

        posts = Posts.objects.filter(ft)

        return posts