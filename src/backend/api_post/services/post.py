from datetime import datetime
from django.db.models import Q, Count
from django.utils.text import slugify
from api_base.services import BaseService
from django.db.models.functions import Lower
from api_post.constants import PostStatus
from api_post.models import Posts, Category, Source
from api_user.constants import Roles
from django.db.models import Avg


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
    def create_list_posts(cls, arr_posts, topic):
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
        if params.get('search'):
            search_string = params.get('search')
            ft &= (Q(author__contains=search_string) | Q(category__title__contains=search_string) | Q(
                title_lower__contains=str(search_string).strip().lower()))
        if params.get('start_date') and params.get('end_date'):
            ft &= Q(publish_date__range=[params.get('start_date'), params.get('end_date')])
        posts = Posts.objects.annotate(title_lower=Lower('title')).filter(ft).prefetch_related(
            'category').prefetch_related('source').prefetch_related('post_rating').annotate(
            avg_rating=Avg("post_rating__star_rating"))
        if params.getlist('categories'):
            topic_ids = params.getlist('categories')
            posts = posts.filter(category__id__in=topic_ids)
        return posts

    @classmethod
    def get_list_post_by_favourite(cls, params=None):
        ft = Q(status=PostStatus.PUBLISHED.value)
        posts = Posts.objects.prefetch_related('post_rating').prefetch_related('category').prefetch_related(
            'source').annotate(avg_rating=Avg('post_rating__star_rating')).filter(ft).order_by('-avg_rating')[:8]
        if params.getlist('categories'):
            topic_ids = params.getlist('categories')
            posts = posts.filter(category__id__in=topic_ids)
        return posts

    @classmethod
    def get_list_post_by_views(cls, params=None):
        ft = Q(status=PostStatus.PUBLISHED.value)
        posts = Posts.objects.filter(ft).prefetch_related('post_rating').prefetch_related('category').prefetch_related(
            'source').annotate(avg_rating=Avg('post_rating__star_rating')).order_by('-views')[:8]
        if params.getlist('categories'):
            topic_ids = params.getlist('categories')
            posts = posts.filter(category__id__in=topic_ids)
        return posts

    @classmethod
    def get_list_post_by_likes(cls, params=None):
        ft = Q(status=PostStatus.PUBLISHED.value)
        posts = Posts.objects.prefetch_related('post_rating').prefetch_related('category').prefetch_related(
            'source').annotate(avg_rating=Avg('post_rating__star_rating')).filter(ft).order_by('-likes')[:8]
        if params.getlist('categories'):
            topic_ids = params.getlist('categories')
            posts = posts.filter(category__id__in=topic_ids)
        return posts

    @classmethod
    def get_list_new_post(cls, params=None):
        ft = Q(status=PostStatus.PUBLISHED.value)
        posts = Posts.objects.prefetch_related('post_rating').prefetch_related('category').prefetch_related(
            'source').annotate(avg_rating=Avg('post_rating__star_rating')).filter(ft).order_by('-publish_date')[:50]
        if params.getlist('categories'):
            topic_ids = params.getlist('categories')
            posts = posts.filter(category__id__in=topic_ids)
        return posts

    @classmethod
    def get_post_management(cls, params=None):
        ft = Q()
        if params.get('search'):
            search_string = params.get('search')
            ft &= (Q(author__contains=search_string) | Q(category__title__contains=search_string) | Q(
                title_lower__contains=str(search_string).strip().lower()))
        if params.get('status'):
            status_string = params.get('status')
            ft &= Q(status=status_string)
        if params.get('start_date') and params.get('end_date'):
            ft &= Q(publish_date__range=[params.get('start_date'), params.get('end_date')])
        posts = Posts.objects.annotate(title_lower=Lower('title')).filter(ft).prefetch_related(
            'category').prefetch_related('source').prefetch_related('post_rating'
                                                                    ).annotate(avg_rating=Avg("post_rating__star_rating"))
        if params.getlist('categories'):
            topic_ids = params.getlist('categories')
            posts = posts.filter(category__id__in=topic_ids)
        return posts

    @classmethod
    def update_status_post(cls, instance):
        posts = Posts.objects.filter(id__in=instance)
        post_update = []
        for post in posts:
            post.status = PostStatus.PUBLISHED.value
            post_update.append(post)
        Posts.objects.bulk_update(post_update, ["status"])
