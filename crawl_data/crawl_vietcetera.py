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

driver.get('https://vietcetera.com/')

list_href = []
posts_urls_temp:List[str] = []
posts_urls = ()
data = []

def get_post(post_url:str, driver: webdriver.Chrome):
    driver.get(post_url)

    title:str = driver.find_element(by=By.XPATH, value="//h1").text
    content:str = driver.find_element(by=By.XPATH, value="//div[contains(@class,'article-content-detail')]").text
    author:str = driver.find_element(by=By.XPATH, value="//a[contains(@href,'/vn/thong-tin-ca-nha')]/span").text
    category:str = driver.find_element(by=By.XPATH, value="//*[@id='article-detail-content-breadcrumb']/a").text
    create_date:str = driver.find_element(by=By.XPATH, value="//span[contains(@class,'styles_articleInfoDateTime')]").text
    likes:str = driver.find_element(by=By.XPATH, value="//button[@aria-label='love button']").text
    thumbnail:str = None
    try:
        thumbnail = driver.find_element(by=By.XPATH,value="//source[@srcset]").get_attribute("srcset")
    except:
        pass
    data.append(dict(Title=title,Category=category,Content=content,Author=author,Create_date=create_date,Likes=likes,Thumbnail=thumbnail))


while len(posts_urls) < 200:
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Xem thêm']")))
    driver.find_element(by=By.XPATH, value="//button[text()='Xem thêm']").click()
    list_href = driver.find_elements(by=By.XPATH, value="//a[starts-with(@href,'/vn/') and contains(@class,'home-latest_articles-article_card-title')]")
    for href in list_href.copy():
        posts_urls_temp.append(href.get_attribute(name="href"))
    posts_urls = set(posts_urls_temp)

for post_url in posts_urls.copy():
    get_post(driver=driver, post_url=post_url)

with open("data-vietcetera.json", "w", encoding='utf-8', newline='') as jsonfile:
    for news in data:
        json_object = json.dumps(news, ensure_ascii=False, indent=4)
        jsonfile.write(json_object)
