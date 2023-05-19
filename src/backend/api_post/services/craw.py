import re

import requests
from bs4 import BeautifulSoup
from django.db import transaction
from api_base.services import BaseService
from bs4.element import Tag
from api_post.models import Keyword, Posts, Contents, Source
from .post import PostService
from .content import ContentService
from .keyword import KeywordService
from utils import Util, Data_Process
from keras import models
import pickle
import core
import os
import after_response

root_url = "https://vietcetera.com"
model_file = os.path.join(core.settings.BASE_DIR, '../AI/models/model_test1')
encoder_file = os.path.join(core.settings.BASE_DIR, '../AI/encoder.pkl')
model = models.load_model(model_file)

with open(encoder_file, 'rb') as f:
    encoder = pickle.load(f)


class CrawlService(BaseService):

    @classmethod
    def crawl_from_url(
            cls, url="https://vietcetera.com"
    ):

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        cards = soup.select('[class*="styles_s-horizontal-card"]')[10:15]
        thumbnails = soup.select('[class*="styles_s-image"] img')
        arr_news = []
        for idx, item in enumerate(cards):
            link = root_url + item.find("a").get("href")
            page_detail = requests.get(link)
            soup_detail = BeautifulSoup(page_detail.content, "html.parser")
            news = {
                "source": link,
                "title": Util.remove_space(
                    soup_detail.select('[class*="articleTitle"]')[0].text
                ),
                "excerpt": Util.remove_space(soup_detail.select('[class*="articleExcerpt"]')[0].text),
                "thumbnail": thumbnails[idx].get("src"),
                "content": [],
                "author": soup_detail.select('[class*="articleAuthorInfo"] span')[0].text,
                "keyword": list(
                    map(
                        lambda x: x.text,
                        soup_detail.select('a[class*="text-inherit"]'),
                    )
                ),
            }
            contents = soup_detail.select('[class*="articleContentDetai"] div')
            i = 0
            for content in contents:
                above_img = False
                item = {
                    "title": "",
                    "paragraph": [],
                    "description_img": "",
                    "image": "",
                    "order": i,
                }
                for child in content.children:
                    paragraph = {
                        "text": "",
                        "above_img": False
                    }
                    if isinstance(child, Tag) and child.name == "h2":
                        item["title"] = Util.remove_space(child.text)
                    elif isinstance(child, Tag) and child.name == "p":
                        paragraph["text"] = Util.remove_space(child.text)
                        paragraph["above_img"] = above_img
                        above_img = False
                        item["paragraph"].append(paragraph)
                    elif isinstance(child, Tag) and child.name == "figure":
                        item["description_img"] = Util.remove_space(child.find("figcaption").text)
                        if type(child.find("img")) != type(None):
                            item["image"] = child.find("img").get("data-srcset")
                            above_img = True

                if item["paragraph"]:
                    news["content"].append(item)
                    i += 1
            arr_news.append(news)
        return arr_news

    @classmethod
    def thread_crawl(cls):
        data = CrawlService.crawl_from_url()
        try:
            data_class = Data_Process(data)
            input_data = data_class.convert_data()
        except Exception as e:
            print("Exception: " + e)
        scores = model.predict(input_data).argmax(axis=-1)
        category = encoder.inverse_transform(scores)
        print(category)
        try:
            with transaction.atomic():
                data, news_data, source = PostService.create_list_posts(data, category)
                Source.objects.bulk_create(
                    source, ignore_conflicts=True
                )
                news_objs = Posts.objects.bulk_create(
                    news_data, ignore_conflicts=True
                )
                keyword_data = KeywordService.create_list_keyword(data, news_objs)
                Keyword.objects.bulk_create(keyword_data, ignore_conflicts=True)
                content_data = ContentService.create_list_content(data, news_objs)
                Contents.objects.bulk_create(content_data, ignore_conflicts=True)
        except Exception as e:
            print("Error: ", e)
        return data

