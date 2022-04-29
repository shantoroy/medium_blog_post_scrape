#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   main.py
@Time    :   2022/04/29 08:25:21
@Author  :   Shanto Roy 
@Version :   1.0
@Contact :   sroy10@uh.edu
@Desc    :   This is the main App file that calls the MediumScrapper Class to 
             perform the scrapping tasks.
'''


import json
import os, errno
from medium_post_scrapper import MediumScrapper
try:
    from local_settings import *
except FileNotFoundError as fx:
    print(str(fx))


if __name__ == '__main__':
    global_tag_list = []
    visited_tag_list = []

    # input initial tag/s in "tag.txt"
    # for snowball effect...
    # let's start by collecting tags continuously from each post, store in a global tag list
    # and run scrapper for each tag that hasn't been visited before (use another list for visited)
    # currently not using it

    with open('tags.txt') as f:
        tag_list = [line.rstrip('\n') for line in f]
        for i in tag_list:
            global_tag_list.append(i)
        global_tag_list = list(set(global_tag_list))
    print("Current Tag List:", list(set(tag_list)))


    # create individual file names for each tag
    file_name_list = [tag+".json" for tag in tag_list]


    # create directory 'data/individual_tag_data' to put individual tag posts
    data_target_dir = "../../../data/individual_tag_data"
    try:
        if not os.path.exists(data_target_dir):
            os.makedirs(data_target_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    # call the scrapper class and start scrapping for tags one after another
    for file_name, tag in zip(file_name_list, tag_list):
        if tag not in visited_tag_list:
            # print(tag)
            scrapper = MediumScrapper(tag, CHROME_DRIVER_PATH=CHROME_DRIVER_PATH)
            output_filename = os.path.join(data_target_dir, file_name)
            try:
                data = scrapper.get_post_contents()
                with open(output_filename, 'w') as fp:
                    json.dump(data, fp)
                
                print("")
                print("==========================================")
                print("Check JSON file: {}".format(output_filename))
                print("Total posts: {}".format(len(data)))
            
            except Exception as e:
                print(str(e))

            visited_tag_list.append(tag)

        
