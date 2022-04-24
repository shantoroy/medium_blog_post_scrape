import time
from bs4 import BeautifulSoup
import requests
from post_details import PostDetais
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MediumScrapper(object):
    def __init__(self, tag, CHROME_DRIVER_PATH='../../chromedriver'):
        self.CHROME_DRIVER_PATH = CHROME_DRIVER_PATH
        self.tag = tag
        content = self.get_intial_content()
        self.parsed_data = BeautifulSoup(content, 'lxml')

    def get_intial_content(self, base_url="https://medium.com/search?q="):
        base_url = base_url + self.tag
        
        options = webdriver.ChromeOptions() 
        options.add_argument("start-maximized")
        options.add_argument('disable-infobars')
        driver = webdriver.Chrome(chrome_options=options, executable_path=r'../../../chromedriver')
        driver.get(base_url)

        initial_XPATH = "//*[@id='root']/div/div[3]/div/div/main/div/div/div/div/div[2]/div[9]/div/div/button"
        max_click_SHOW_MORE = 2
        count = 1 

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()

        while count < max_click_SHOW_MORE:
            try:
                time.sleep(10)
                new_XPATH = initial_XPATH[:67] + str(count) + initial_XPATH[67:]
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, new_XPATH))).click()
                print("Button clicked #", count+1)
                count += 1
            except TimeoutException:
                break

        time.sleep(1.5)
        content = driver.execute_script(
                    "return document.documentElement.outerHTML")
        driver.quit()
        return content


    ## return list of post links
    def get_post_links(self):
        post_details = PostDetais(self.parsed_data)
        json_data = json.loads(post_details.json_response_whole())

        # dictionary_view
        # post_keys = {key:value["mediumUrl"] for key,value in json_data.items() if key.startswith("Post:")}
        
        # we will collect a list of URLs
        post_URL_list = [value["mediumUrl"] for key,value in json_data.items() if key.startswith("Post:")]
        return post_URL_list

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
                post_tags = post_details.get_tags(first_key_element, json_full_script)
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

                # for collecting tags using the snowball mathod
                textfile = open("tags.txt", "a")
                for element in post_tags:
                    textfile.write(element + "\n")
                textfile.close()

            except Exception as e:
                print("Error in scrapping link: {}".format(link))
                print(str(e))
        return data
