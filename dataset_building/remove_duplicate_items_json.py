#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   remove_duplicate_items_json.py
@Time    :   2022/05/01 21:15:00
@Author  :   Shanto Roy 
@Version :   1.0
@Contact :   sroy10@uh.edu
@Desc    :   This script removes the duplicate posts
'''


import json
import os

path = os.path.join(os.getcwd(), "data")

input_filename = "integrated_all_post_data_final.json"

with open(os.path.join(path,input_filename), "r") as f:
    data = json.load(f)
unique_post = {each['title']: each for each in data}
listed_dictionary_items = list(unique_post.values())

# word_dict = {"food": "truffle"}
# for i in word_dict:
#     count = 0
#     for key in listed_dictionary_items:
#         if i in key['content'] and word_dict[i] in key['content']:
#             listed_dictionary_items.remove(key)
#     print("Number of Final posts:", len(listed_dictionary_items))

output_filename = "related_data_rm_duplicacy_final.json"

with open(os.path.join(path,output_filename), "w") as f:
    json.dump(listed_dictionary_items, f)
print("# of post after removing duplicacy = ", len(listed_dictionary_items))
