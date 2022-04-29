#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   medium_post_scrapper.py
@Time    :   2022/04/29 08:42:57
@Author  :   Shanto Roy 
@Version :   1.0
@Contact :   sroy10@uh.edu
@Desc    :   This file provides a class for scrolling down 
             a medium query page to collect post links
'''


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

    def get_intial_content(self, base_url="https://medium.com/search?q="):
        base_url = base_url + self.tag
        
        options = webdriver.ChromeOptions() 
        options.add_argument("start-maximized")
        options.add_argument('disable-infobars')
        driver = webdriver.Chrome(chrome_options=options, executable_path=r'../../../../chromedriver')
        driver.get(base_url)

        # there are two types of XPATHs present in Medium 'Show More' Buttons
        initial_XPATH1 = "//*[@id='root']/div/div[3]/div/div/main/div/div/div/div/div[2]/div[9]/div/div/button"
        initial_XPATH2 = "//*[@id='root']/div/div[3]/div/div/main/div/div/div/div/div[2]/div[10]/div/div/button"
        max_click_SHOW_MORE = 500
        count = 1 

        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, initial_XPATH1))).click()

            while count < max_click_SHOW_MORE:
                try:
                    time.sleep(10)
                    # adding a substring (increasing integer) before 9 so that we get -> 19,29,39,49,...
                    new_XPATH = initial_XPATH1[:67] + str(count) + initial_XPATH1[67:]
                    print(new_XPATH)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, new_XPATH))).click()
                    print("Button clicked #", count+1)
                    count += 1
                except TimeoutException:
                    break
                    
        except Exception as e:
            print("Xpath 1 does not work... switching to Xpath2")

        finally:
            count = 2
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, initial_XPATH2))).click()

            while count < max_click_SHOW_MORE:
                try:
                    time.sleep(10)
                    # adding a substring (increasing integer) before 9 so that we get -> 19,29,39,49,...
                    new_XPATH = initial_XPATH2[:67] + str(count) + initial_XPATH2[68:]
                    print(new_XPATH)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, new_XPATH))).click()
                    print("Button clicked #", count)
                    count += 1
                except TimeoutException:
                    break
        
        # the following no longer works since it outputs only source from initial load of URL
        # that means we only get first 9 articles
        # content = driver.execute_script("return document.documentElement.outerHTML")  

        article_max_possible_ID = (count-1) * 10 + 9
        article_count = 1
        link_list = []

        # this xpath was obtained by copying xpath by inspecting post title `a` tag
        init_article_XPATH = '//*[@id="root"]/div/div[3]/div/div/main/div/div/div/div/div[2]/div[1]/article/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div[1]/div[1]/a'

        while article_count <= article_max_possible_ID:
            # replacing 1 with all increasing integer values, we get 1,2,3,... for div[] right before `article`
            new_article_XPATH = init_article_XPATH[:67] + str(article_count) + init_article_XPATH[68:]
            
            # help : https://stackoverflow.com/questions/12579061/python-selenium-find-object-attributes-using-xpath
            for element in driver.find_elements(By.XPATH, new_article_XPATH):
                try:
                    link_list.append(element.get_attribute('href'))
                except Exception as e:
                    print(str(e))
            article_count += 1
        
        driver.quit()

        # pre-process article links
        # example link: 'https://medium.com/@beyondprotocol/bp-now-available-on-metamask-\
        #                       swap-c0d111cf6dd4?source=search_post---------0----------------------------'
        # need to remove contents from `?source`
        mod_link_list = []
        for link in link_list:
            try:
                target = link.find("?source")
                link = link[:target]
                mod_link_list.append(link)
            except Exception as e:
                print(str(e))

        return mod_link_list


    # collect list of links
    # browse each post link and store contents in JSON format
    def get_post_contents(self):
        links = self.get_intial_content()
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
