import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from post_details import PostDetais
import json


class MediumScrapper(object):
    def __init__(self, tag, CHROME_DRIVER_PATH='../../chromedriver'):
        self.CHROME_DRIVER_PATH = CHROME_DRIVER_PATH
        self.tag = tag
        content = self.get_intial_content()
        self.parsed_data = BeautifulSoup(content, 'lxml')

    def get_intial_content(self, base_url="https://medium.com/search?q="):
        base_url = base_url + self.tag
        driver = webdriver.Chrome(self.CHROME_DRIVER_PATH)
        driver.get(base_url)
        scrolls = 300
        while scrolls > 0:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight-1000);")
            time.sleep(2)
            scrolls -= 1
        # driver.implicitly_wait(30)
        time.sleep(1.5)
        content = driver.execute_script(
            "return document.documentElement.outerHTML")
        driver.quit()
        return content

    def get_post_links(self):
        links = []
        class_names = "button button--smaller button--chromeless u-baseColor--buttonNormal"
        for my_tag in self.parsed_data.find_all(class_=class_names):
            links.append(my_tag.get('href'))
        return links

    def get_post_contents(self):
        links = self.get_post_links()
        data = []
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        count = 0
        for link in links:
            try:
                count += 1
                print("Scrapping link {}: {}".format(count, link))
                time.sleep(1)
                request_link = requests.get(link, headers=headers)
                request_content = BeautifulSoup(request_link.content,
                                                'html.parser')
                post_details = PostDetais(request_content, link)
                """
                ### we're going to collect both json scripts first
                ### also the key we'll require to extract latter infos
                """
                json_basic_script = json.loads(post_details.json_response_basic())
                json_full_script = json.loads(post_details.json_response_whole())
                first_key_element = post_details.find_first_key(json_full_script)
                """
                ### now we'll collect all the info we need
                """
                post_title = post_details.get_title()
                author_name, author_link = post_details.get_author_name(json_basic_script)
                creation_date, published_date, modified_date = post_details.get_date(json_basic_script)
                post_tags = post_details.get_tags(json_basic_script)
                post_readtime = post_details.get_read(first_key_element, json_full_script)
                post_claps, post_voters = post_details.get_upvote(first_key_element, json_full_script)
                post_contents = post_details.get_post_content()
                post_responses = post_details.get_response(first_key_element, json_full_script)
                single_post = {
                    "title": post_title,
                    "post_link": link,
                    "author_name": author_name,
                    "author_link": author_link,
                    "publish_date": published_date[:10],
                    "last_modified_date": modified_date[:10],
                    "readtime": (str(post_readtime))[:4],
                    "claps": post_claps,
                    "voters": post_voters,
                    "content": post_contents,
                    "responses": post_responses,
                    "tags": post_tags
                }
                data.append(single_post)
            except Exception as e:
                print("Error in scrapping link: {}".format(link))
                print(str(e))
        return data
