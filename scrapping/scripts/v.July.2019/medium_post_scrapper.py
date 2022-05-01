import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from post_details import PostDetais


class MediumScrapper(object):
    def __init__(self, CHROME_DRIVER_PATH='/home/mrx/Downloads/chromedriver'):
        self.CHROME_DRIVER_PATH = CHROME_DRIVER_PATH
        content = self.get_intial_content()
        self.parsed_data = BeautifulSoup(content, 'lxml')

    def get_intial_content(self,
                           base_url="https://medium.com/search?q=ripple"):
        driver = webdriver.Chrome(self.CHROME_DRIVER_PATH)
        driver.get(base_url)
        scrolls = 50
        while scrolls > 0:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight-1000);")
            time.sleep(15)
            scrolls -= 1
        # driver.implicitly_wait(30)
        time.sleep(30)
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
        for link in links:
            try:
                print("Scrapping link: {}".format(link))
                time.sleep(15)
                request_link = requests.get(link, headers=headers)
                request_content = BeautifulSoup(request_link.content,
                                                'html.parser')
                post_details = PostDetais(request_content, link)
                post_title = post_details.get_title()
                author_name = post_details.get_author_name()
                post_date = post_details.get_date()
                post_readtime = post_details.get_read()
                post_upvotes = post_details.get_upvote()
                post_contents = post_details.get_post_content()
                post_responses = post_details.get_response()
                single_post = {
                    "title": post_title,
                    "author_name": author_name,
                    "link": link,
                    "post_date": post_date,
                    "readtime": post_readtime,
                    "upvotes": post_upvotes,
                    "content": post_contents,
                    "responses": post_responses
                }
                data.append(single_post)
            except Exception as e:
                print("Error in scrapping link: {}".format(link))
                print(str(e))
        return data
