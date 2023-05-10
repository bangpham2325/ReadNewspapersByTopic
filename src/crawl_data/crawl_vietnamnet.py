from typing import List
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
wait = WebDriverWait(driver, 10)

web_url = 'https://vietnamnet.vn/'
driver.get(web_url)

list_href = []
items_urls:List[str] = []
posts_urls_temp:List[str] = []
posts_urls = ()
data = []

def get_post(post_url:str, driver: webdriver.Chrome):
    driver.get(post_url)
    try:
        title: str = driver.find_element(by=By.XPATH, value="//h1").text
        content: str = driver.find_element(by=By.XPATH, value="//*[@id='maincontent']").text
        author: str = driver.find_element(by=By.XPATH, value="//p[@class='article-detail-author__info']/span[@class='name']").text
        category: str = driver.find_element(by=By.XPATH,value="//div[@class='bread-crumb-detail ']/ul/li[2]").text
        create_date: str = driver.find_element(by=By.XPATH, value="//div[@class='bread-crumb-detail__time']/p").text
        likes: str = None
        thumbnail: str = driver.find_element(by=By.XPATH,value="//figure[contains(@class,'vnn-content-image')]/img").get_attribute("src")
        data.append(
            dict(Title=title, Category=category, Content=content, Author=author, Create_date=create_date, Likes=likes,
                 Thumbnail=thumbnail))
    except:
        pass


def get_urls_by_category(url:str, driver: webdriver.Chrome):
    driver.get(url)

    list_href = driver.find_elements(by=By.XPATH, value="//div[contains(@class,'horizontalPost__avt')]/a")
    for href in list_href.copy():
        url = href.get_attribute(name="href")
        posts_urls_temp.append(url)


category = driver.find_elements(by=By.XPATH, value="//ul[@class='header_submenu-content-list']/li/a")

for category_link in category:
    url = category_link.get_attribute("href")
    if ('premium' in url) or ('en' in url) or ('talkshow' in url) or ('podcast' in url) or ('download-app' in url):
        continue
    items_urls.append(url)

for url in items_urls.copy():
    get_urls_by_category(url=url, driver=driver)

posts_urls = set(posts_urls_temp)

for post_url in posts_urls.copy():
    get_post(driver=driver, post_url=post_url)

with open("data-vietnamnet.json", "w", encoding='utf-8', newline='') as jsonfile:
    for news in data:
        json_object = json.dumps(news, ensure_ascii=False, indent=4)
        jsonfile.write(json_object)
