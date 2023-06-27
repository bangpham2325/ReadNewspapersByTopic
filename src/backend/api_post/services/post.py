from datetime import datetime
from django.db.models import Q, Count
from django.utils.text import slugify
from api_base.services import BaseService
from django.db.models.functions import Lower
from api_post.constants import PostStatus
from api_post.models import Posts, Category, Source
from api_user.constants import Roles
from django.db.models import Avg
from api_base.services import CloudinaryService


class PostService(BaseService):
    @classmethod
    def create_post(cls, data):
        keyword = data.pop('keywords') if "keywords" in data else []
        post_obj = Posts(**data)
        post_obj.slug = slugify(f"{post_obj.title[:30]} {post_obj.id.hex[:5]}")
        post_obj.save()
        from api_post.services import KeywordService
        KeywordService.create_list_keyword_for_post(keyword, post_obj.id)
        return post_obj

    @classmethod
    def upload_avatar(cls, image):
        upload_data = CloudinaryService.upload_thumb_post_image(image)
        return upload_data.get("url")

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
    def get_list_post_by_category(cls, params=None, category_ids=None):
        ft = Q(status=PostStatus.PUBLISHED.value)
        ft &= Q(user__isnull=True)
        if params.get('categories'):
            topic_ids = params.get('categories')
            ft &= Q(category__id=topic_ids)
        elif category_ids is not None:
            ft &= Q(category__id__in=category_ids)
        if params.get('search'):
            search_string = params.get('search')
            ft &= (Q(author__icontains=search_string) | Q(category__title__icontains=search_string) | Q(
                title_lower__contains=str(search_string).strip().lower()))
        if params.get('start_date') and params.get('end_date'):
            ft &= Q(publish_date__range=[params.get('start_date'), params.get('end_date')])
        posts = Posts.objects.annotate(title_lower=Lower('title')).filter(ft).prefetch_related(
            'category', 'user', 'source', 'post_rating').annotate(
            avg_rating=Avg("post_rating__star_rating")).order_by('-publish_date')
        return posts

    @classmethod
    def get_list_post_by_favourite(cls, category_ids=None):
        ft = Q(status=PostStatus.PUBLISHED.value)
        ft &= Q(user__isnull=True)
        if category_ids is not None:
            ft &= Q(category__id__in=category_ids)
        posts = Posts.objects.prefetch_related(
            'category', 'user', 'source', 'post_rating').annotate(avg_rating=Avg('post_rating__star_rating')).filter(ft).order_by('-avg_rating')[:8]
        return posts

    @classmethod
    def get_list_post_by_views(cls, category_ids=None):
        ft = Q(status=PostStatus.PUBLISHED.value)
        ft &= Q(user__isnull=True)
        if category_ids is not None:
            ft &= Q(category__id__in=category_ids)
        posts = Posts.objects.filter(ft).prefetch_related(
            'category', 'user', 'source', 'post_rating').annotate(avg_rating=Avg('post_rating__star_rating')).order_by('-views')[:8]
        return posts

    @classmethod
    def get_list_post_by_likes(cls, category_ids=None):
        ft = Q(status=PostStatus.PUBLISHED.value)
        ft &= Q(user__isnull=True)
        if category_ids is not None:
            ft &= Q(category__id__in=category_ids)
        posts = Posts.objects.prefetch_related(
            'category', 'user', 'source', 'post_rating').annotate(avg_rating=Avg('post_rating__star_rating')).filter(ft).order_by('-likes')[:8]
        return posts

    @classmethod
    def get_list_new_post(cls, params=None, category_ids=None):
        ft = Q(status=PostStatus.PUBLISHED.value)
        ft &= Q(user__isnull=True)
        if params.get('categories'):
            topic_ids = params.get('categories')
            ft &= Q(category__id=topic_ids)
        elif category_ids is not None:
            ft &= Q(category__id__in=category_ids)
        if params.get('search'):
            search_string = params.get('search')
            ft &= (Q(author__contains=search_string) | Q(category__title__contains=search_string) | Q(
                title_lower__contains=str(search_string).strip().lower()))
        posts = Posts.objects.prefetch_related(
            'category', 'user', 'source', 'post_rating').annotate(avg_rating=Avg('post_rating__star_rating')).filter(ft).order_by('-publish_date')[:50]
        return posts

    @classmethod
    def get_post_by_author(cls, user_id):
        ft = Q(status=PostStatus.PUBLISHED.value)
        ft &= Q(user__id=user_id)
        posts = Posts.objects.prefetch_related(
            'category', 'user', 'source', 'post_rating').annotate(avg_rating=Avg('post_rating__star_rating')).filter(ft).order_by('-publish_date')
        return posts

    @classmethod
    def get_post_management(cls, params=None):
        ft = Q()
        if params.getlist('categories'):
            topic_ids = params.getlist('categories')
            ft &= Q(category__id__in=topic_ids)
        if params.get('search'):
            search_string = params.get('search')
            ft &= (Q(author__contains=search_string) | Q(category__title__contains=search_string) | Q(
                title_lower__contains=str(search_string).strip().lower()))
        if params.get('status'):
            status_string = params.get('status')
            if status_string == 'DRAFT':
                ft &= Q(user__isnull=True)
            ft &= Q(status=status_string)
        if params.get('start_date') and params.get('end_date'):
            ft &= Q(publish_date__range=[params.get('start_date'), params.get('end_date')])
        posts = Posts.objects.annotate(title_lower=Lower('title')).filter(ft).prefetch_related(
            'category', 'user', 'source', 'post_rating').annotate(avg_rating=Avg("post_rating__star_rating")).order_by('-created_at')
        return posts

    @classmethod
    def get_post_management_author(cls, params=None):
        ft = Q(user__isnull=False)
        ft &= Q(status__in=[PostStatus.PUBLISHED.value, PostStatus.PENDING.value])
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
            'category', 'user', 'source', 'post_rating').annotate(avg_rating=Avg("post_rating__star_rating")).order_by('-created_at')
        return posts

    @classmethod
    def list_my_post(cls, params, user_id):
        ft = Q(user__id=user_id)
        if params.get('categories'):
            topic_ids = params.get('categories')
            ft &= Q(category__id=topic_ids)
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
            'category', 'user', 'source', 'post_rating').annotate(avg_rating=Avg("post_rating__star_rating")).order_by('-created_at')
        return posts

    @classmethod
    def list_blog(cls, params):
        ft = Q(user__isnull=False)
        ft &= Q(status=PostStatus.PUBLISHED.value)
        if params.get('categories'):
            topic_ids = params.get('categories')
            ft &= Q(category__id=topic_ids)
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
            'category', 'user', 'source', 'post_rating').annotate(avg_rating=Avg("post_rating__star_rating")).order_by('-created_at')[:50]
        return posts

    @classmethod
    def update_status_post(cls, instance):
        posts = Posts.objects.filter(id__in=instance)
        post_update = []
        for post in posts:
            post.status = PostStatus.PUBLISHED.value
            post_update.append(post)
        Posts.objects.bulk_update(post_update, ["status"])

    @classmethod
    def get_post_author(cls, params=None):
        ft = Q(user__isnull=False)
        ft &= Q(status__in=PostStatus.PUBLISHED.value)
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
            'category', 'user', 'source', 'post_rating').annotate(avg_rating=Avg("post_rating__star_rating")).order_by('-created_at')
        if params.getlist('categories'):
            topic_ids = params.getlist('categories')
            posts = posts.filter(category__id__in=topic_ids)
        return posts
