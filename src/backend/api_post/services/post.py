from datetime import datetime
from django.db.models import Q
from django.utils.text import slugify
from api_base.services import BaseService
from django.db.models.functions import Lower
from api_post.constants import PostStatus
from api_post.models import Posts


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

        courses = Posts.objects.filter(**ft)
        # process_ids = [item[0] for item in list(process_courses.values_list('course_id'))]
        # courses = courses.filter(id__in=process_ids)

        return courses
