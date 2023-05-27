import re

import numpy as np
import requests
from bs4 import BeautifulSoup
from django.db import transaction
from api_base.services import BaseService
from bs4.element import Tag
from api_post.models import Keyword, Posts, Contents, Source, PostVector
from .post import PostService
from .post_vector import PostVectorService
from .content import ContentService
from .keyword import KeywordService
from utils import Util, Data_Process
from keras import models
import pickle
import core
import os
from django.core.files.storage import default_storage


import after_response

root_url_vietcetera = "https://vietcetera.com"
root_url_dantri = "https://dantri.com.vn/tin-moi-nhat.htm"
root_url_vnexpress = "https://vnexpress.net/tin-tuc-24h"
root_url_vietnamnet = "https://vietnamnet.vn"
file_path = 'tfidf_vectors.pkl'

model_file = os.path.join(core.settings.BASE_DIR, '../AI/models/model_test2')
encoder_file = os.path.join(core.settings.BASE_DIR, '../AI/encoder.pkl')
model = models.load_model(model_file)
pattern = r"(https:\S+)(?=\s?2x|,)"

with open(encoder_file, 'rb') as f:
    encoder = pickle.load(f)


class CrawlService(BaseService):

    @classmethod
    def crawl_from_url_vietcetera(
            cls, url=root_url_vietcetera
    ):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        cards = soup.select('[class*="styles_s-horizontal-card"][class*="rounded-12pt p-16pt styles_s-card"]')[0:20]
        arr_news = []
        for idx, item in enumerate(cards):
            try:
                link = url + item.find("a").get("href")

                try:
                    source_list = [item['source'] for item in arr_news]
                    if link in source_list:
                        continue
                except:
                    pass
                page_detail = requests.get(link)
                soup_detail = BeautifulSoup(page_detail.content, "html.parser")
                news = {
                    "source": link,
                    "title": Util.remove_space(
                        soup_detail.select('[class*="articleTitle"]')[0].text
                    ),
                    "excerpt": Util.remove_space(soup_detail.select('[class*="articleExcerpt"]')[0].text),
                    "thumbnail": item.find('figure').find('img').get("src"),
                    "content": [],
                    "author": Util.remove_space(soup_detail.select('[class*="articleAuthorInfo"] span')[0].text),
                    "keyword": list(
                        map(
                            lambda x: Util.remove_space(x.text),
                            soup_detail.select('a[class*="text-inherit"]'),
                        )
                    ),
                }
                contents = soup_detail.select('[class*="articleContentDetai"] div')
                i = 0
                for content in contents:
                    below_img = False
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
                            "below_img": False
                        }
                        if isinstance(child, Tag) and child.name == "h2":
                            item["title"] = Util.remove_space(child.text)
                        elif isinstance(child, Tag) and child.name == "p":
                            paragraph["text"] = Util.remove_space(child.text)
                            paragraph["below_img"] = below_img
                            below_img = False
                            item["paragraph"].append(paragraph)
                        elif isinstance(child, Tag) and child.name == "figure":
                            item["description_img"] = Util.remove_space(child.find("figcaption").text)
                            if type(child.find("img")) != type(None):
                                item["image"] = child.find("img").get("data-srcset")
                                try:
                                    item["paragraph"][-1]["below_img"] = True
                                except:
                                    item["paragraph"].append(paragraph)
                                    item["paragraph"][-1]["below_img"] = True

                    if item["paragraph"]:
                        news["content"].append(item)
                        i += 1
                arr_news.append(news)
            except:
                continue
        return arr_news

    @classmethod
    def crawl_from_url_dantri(
            cls, url=root_url_dantri
    ):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        cards = soup.select('[class*="article-list article-item"]')[0:20]
        thumbnails = soup.select('[class*="article-thumb"] img')
        arr_news = []
        for idx, item in enumerate(cards):
            try:
                link = url + item.find("a").get("href")
                page_detail = requests.get(link)
                soup_detail = BeautifulSoup(page_detail.content, "html.parser")
                data_srcset = item.find("div", {"class": "article-thumb"}).find("img").get("srcset")
                if data_srcset is None:
                    thumbnails_image = item.find("div", {"class": "article-thumb"}).find("img").get("src")
                else:
                    thumbnails_re = re.findall(pattern, data_srcset)
                    thumbnails_image = thumbnails_re[0]
                news = {
                    "source": link,
                    "title":
                        Util.remove_space(soup_detail.select('[class*="title-page"]')[0].text)
                    ,
                    "excerpt": Util.remove_space(soup_detail.select('[class*="singular-sapo"]')[0].text),
                    "thumbnail": thumbnails_image,
                    "content": [],
                    "author": Util.remove_space(soup_detail.select('[class*="author-name"] b')[0].text),
                    "keyword": list(
                        map(
                            lambda x: Util.remove_space(x.text),
                            soup_detail.select('a[data-content-name*="article-tags"]'),
                        )
                    ),
                }
                contents = soup_detail.select('[class*="singular-content"]')[0]
                i = 0
                below_img = False
                item = {
                    "title": "",
                    "paragraph": [],
                    "description_img": "",
                    "image": "",
                    "order": i,
                }
                for child in contents.children:
                    paragraph = {
                        "text": "",
                        "below_img": False
                    }
                    if isinstance(child, Tag) and type(child.find("strong")) != type(None):
                        if item["paragraph"]:
                            news["content"].append(item)
                            i += 1
                            item = {
                                "title": "",
                                "paragraph": [],
                                "description_img": "",
                                "image": "",
                                "order": i,
                            }
                        item["title"] = Util.remove_space(child.find("strong").text)
                        if child.name == "p":
                            paragraph["text"] = Util.remove_space(child.text)
                            paragraph["below_img"] = below_img
                            item["paragraph"].append(paragraph)
                    elif isinstance(child, Tag) and child.name == "p":
                        if item["paragraph"] and item["description_img"]:
                            news["content"].append(item)
                            i += 1
                            item = {
                                "title": "",
                                "paragraph": [],
                                "description_img": "",
                                "image": "",
                                "order": i,
                            }
                        paragraph["text"] = Util.remove_space(child.text)
                        paragraph["below_img"] = below_img
                        item["paragraph"].append(paragraph)
                    elif isinstance(child, Tag) and child.name == "figure":
                        item["description_img"] = Util.remove_space(child.find("figcaption").text)
                        if type(child.find("img")) != type(None):
                            data_srcset = child.find("img").get("data-srcset")
                            if data_srcset is None:
                                item["image"] = child.find("img").get("data-src")
                            else:
                                thumbnails_re = re.findall(pattern, data_srcset)
                                item["image"] = thumbnails_re[0]
                            if item["paragraph"]:
                                item["paragraph"][-1]["below_img"] = True
                            else:
                                news["content"].append(item)
                                i += 1
                                item = {
                                    "title": "",
                                    "paragraph": [],
                                    "description_img": "",
                                    "image": "",
                                    "order": i,
                                }

                if item["paragraph"]:
                    news["content"].append(item)
                    i += 1
                arr_news.append(news)
            except:
                continue
        return arr_news

    @classmethod
    def crawl_from_url_vnexpress(
            cls, url=root_url_vnexpress
    ):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        cards = soup.select('[class*="item-news item-news-common"]')[0:20]
        # thumbnails = soup.select('[class*="thumb-art"] img')
        arr_news = []
        for idx, item in enumerate(cards):
            try:
                link = item.find("a").get("href")
                page_detail = requests.get(link)
                soup_detail = BeautifulSoup(page_detail.content, "html.parser")
                try:
                    author = soup_detail.select('p[class*="Normal"][style*="text-align:right"] strong')[0].text
                except:
                    author = soup_detail.select('p[class*="author_mail"] strong')[0].text
                # Extract the value of srcset or data-srcset attribute
                source_tag = item.find("picture").find("img").find_previous_sibling('source')
                if 'srcset' in source_tag.attrs:
                    data_srcset = source_tag['srcset']
                elif 'data-srcset' in source_tag.attrs:
                    data_srcset = source_tag['data-srcset']
                else:
                    data_srcset = None
                if data_srcset is None:
                    thumbnails_image = item.find("picture").find("img").get("src")
                else:
                    thumbnails_re = re.findall(pattern, data_srcset)
                    thumbnails_image = thumbnails_re[0]
                news = {
                    "source": link,
                    "title":
                        Util.remove_space(soup_detail.select('[class*="title-detail"]')[0].text)
                    ,
                    "excerpt": Util.remove_space(soup_detail.select('[class*="description"]')[0].text),
                    "thumbnail": thumbnails_image,
                    "content": [],
                    "author": Util.remove_space(author),
                    "keyword": list(
                        map(
                            lambda x: Util.remove_space(x.text),
                            soup_detail.select('[class*="item-tag"] a'),
                        )
                    ),
                }
                contents = soup_detail.select('[class*="fck_detail"]')[0]
                i = 0
                below_img = False
                item = {
                    "title": "",
                    "paragraph": [],
                    "description_img": "",
                    "image": "",
                    "order": i,
                }
                for child in contents.children:
                    paragraph = {
                        "text": "",
                        "below_img": False
                    }
                    if isinstance(child, Tag) and type(child.find("strong")) != type(None):
                        if item["paragraph"]:
                            news["content"].append(item)
                            i += 1
                            item = {
                                "title": "",
                                "paragraph": [],
                                "description_img": "",
                                "image": "",
                                "order": i,
                            }
                        item["title"] = Util.remove_space(child.find("strong").text)
                        if child.name == "p":
                            paragraph["text"] = Util.remove_space(child.text)
                            paragraph["below_img"] = below_img
                            item["paragraph"].append(paragraph)

                    elif isinstance(child, Tag) and child.name == "p":
                        if item["paragraph"] and item["description_img"]:
                            news["content"].append(item)
                            i += 1
                            item = {
                                "title": "",
                                "paragraph": [],
                                "description_img": "",
                                "image": "",
                                "order": i,
                            }
                        paragraph["text"] = Util.remove_space(child.text)
                        paragraph["below_img"] = below_img
                        item["paragraph"].append(paragraph)
                    elif isinstance(child, Tag) and child.name == "figure":
                        item["description_img"] = Util.remove_space(child.find("figcaption").text)
                        if type(child.find("img")) != type(None):
                            source_tag = child.find("img").find_previous_sibling('source')
                            if 'srcset' in source_tag.attrs:
                                data_srcset = source_tag['srcset']
                            elif 'data-srcset' in source_tag.attrs:
                                data_srcset = source_tag['data-srcset']
                            else:
                                data_srcset = None
                            if data_srcset is None:
                                item["image"] = child.find("img").get("data-src")
                            else:
                                thumbnails_re = re.findall(pattern, data_srcset)
                                item["image"] = thumbnails_re[0]
                            if item["paragraph"]:
                                item["paragraph"][-1]["below_img"] = True
                            else:
                                news["content"].append(item)
                                i += 1
                                item = {
                                    "title": "",
                                    "paragraph": [],
                                    "description_img": "",
                                    "image": "",
                                    "order": i,
                                }

                if item["paragraph"]:
                    news["content"].append(item)
                    i += 1
                arr_news.append(news)
            except:
                continue
        return arr_news

    @classmethod
    def crawl_from_url_vietnamnet(
            cls, url="https://vietnamnet.vn/tin-moi-nong"
    ):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        cards = soup.select('[class*="horizontalPost"][class*="mb-20"]')[0:20]
        thumbnails = soup.select('[class*="horizontalPost__avt"] img')
        arr_news = []
        for idx, item in enumerate(cards):
            try:
                link = root_url_vietnamnet + item.find("a").get("href")
                page_detail = requests.get(link)
                soup_detail = BeautifulSoup(page_detail.content, "html.parser")
                thumbnails_image = item.find("a").find("img").get("src")
                news = {
                    "source": link,
                    "title":
                        Util.remove_space(soup_detail.select('[class*="content-detail-title"]')[0].text)
                    ,
                    "excerpt": Util.remove_space(soup_detail.select('[class*="content-detail-sapo"]')[0].text),
                    "thumbnail": thumbnails_image,
                    "content": [],
                    "author": Util.remove_space(soup_detail.select('[class*="article-detail-author__info"] a')[0].text),
                    "keyword": list(
                        map(
                            lambda x: Util.remove_space(x.text),
                            soup_detail.select('[class*="tag"] a'),
                        )
                    ),
                }
                contents = soup_detail.select('[class*="main-content"]')[0]
                i = 0
                below_img = False
                item = {
                    "title": "",
                    "paragraph": [],
                    "description_img": "",
                    "image": "",
                    "order": i,
                }
                for child in contents.children:
                    paragraph = {
                        "text": "",
                        "below_img": False
                    }
                    if isinstance(child, Tag) and type(child.find("strong")) != type(None):
                        if item["paragraph"]:
                            news["content"].append(item)
                            i += 1
                            item = {
                                "title": "",
                                "paragraph": [],
                                "description_img": "",
                                "image": "",
                                "order": i,
                            }
                        item["title"] = Util.remove_space(child.find("strong").text)
                        if child.name == "p":
                            paragraph["text"] = Util.remove_space(child.text)
                            paragraph["below_img"] = below_img
                            item["paragraph"].append(paragraph)
                    elif isinstance(child, Tag) and child.name == "p":
                        if item["paragraph"] and item["description_img"]:
                            news["content"].append(item)
                            i += 1
                            item = {
                                "title": "",
                                "paragraph": [],
                                "description_img": "",
                                "image": "",
                                "order": i,
                            }
                        paragraph["text"] = Util.remove_space(child.text)
                        paragraph["below_img"] = below_img
                        item["paragraph"].append(paragraph)
                    elif isinstance(child, Tag) and child.name == "figure":
                        item["description_img"] = Util.remove_space(child.find("figcaption").text)
                        if type(child.find("img")) != type(None):
                            item["image"] = child.find("img").get("src")
                            if item["paragraph"]:
                                item["paragraph"][-1]["below_img"] = True
                            else:
                                news["content"].append(item)
                                i += 1
                                item = {
                                    "title": "",
                                    "paragraph": [],
                                    "description_img": "",
                                    "image": "",
                                    "order": i,
                                }
                if item["paragraph"]:
                    news["content"].append(item)
                    i += 1
                arr_news.append(news)
            except:
                continue
        return arr_news

    @classmethod
    def craw_and_save_data_in_db(cls, data):
        try:
            in_db_sources = Source.objects.values_list("domain", flat=True)
            data = list(
                filter(lambda x: x.get("source") not in in_db_sources, data)
            )
            if not data:
                return
            data_class = Data_Process(data)
            input_data = data_class.convert_data()
            if os.path.exists(file_path):
                # Load the existing data from the file
                file = default_storage.open(file_path, 'rb')
                # Read the file content as bytes
                file_content = file.read()
                # Load the data from the file content
                tfidf_vectors_svd = pickle.loads(file_content)
                # with open(file_path, 'rb') as file:
                #     existing_data = pickle.load(file)
                # Combine the existing data with the new data
                combined_data = np.concatenate((tfidf_vectors_svd, input_data), axis=0)
            else:
                combined_data = input_data  # No existing data, use only the new data

            # Save the combined data to the file, overwriting it
            with open(file_path, 'wb') as file:
                pickle.dump(combined_data, file)

            with open(file_path, 'rb') as file:
                try:
                    default_storage.save(file_path, file)
                    print("File uploaded successfully!")
                except Exception as e:
                    print("An error occurred while uploading the file:", str(e))

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
                post_vector = PostVectorService.create_list_post_vector(input_data, news_objs)
                # Bulk create the news vectors
                PostVector.objects.bulk_create(post_vector)
                keyword_data = KeywordService.create_list_keyword(data, news_objs)
                Keyword.objects.bulk_create(keyword_data, ignore_conflicts=True)
                content_data = ContentService.create_list_content(data, news_objs)
                Contents.objects.bulk_create(content_data, ignore_conflicts=True)
        except Exception as e:
            print("Error: ", e)
        return data

def thread_crawl_vietcetera():
    data_vietcetera = CrawlService.crawl_from_url_vietcetera()
    CrawlService.craw_and_save_data_in_db(data_vietcetera)


def thread_crawl_dantri():
    data_dantri = CrawlService.crawl_from_url_dantri()
    CrawlService.craw_and_save_data_in_db(data_dantri)


def thread_crawl_vnexpress():
    data_vnexpress = CrawlService.crawl_from_url_vnexpress()
    CrawlService.craw_and_save_data_in_db(data_vnexpress)


def thread_crawl_vietnamnet():
    data_vietnamnet = CrawlService.crawl_from_url_vietnamnet()
    CrawlService.craw_and_save_data_in_db(data_vietnamnet)
