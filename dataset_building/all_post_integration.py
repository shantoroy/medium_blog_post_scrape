#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   all_post_integration.py
@Time    :   2022/05/01 20:47:26
@Author  :   Shanto Roy 
@Version :   1.0
@Contact :   sroy10@uh.edu
@Desc    :   This program integrates all the relevant posts from
             JSON files for each keyword. We check relevancy by searching
             the keyword either in title or in tag. The program also
             prints the number of relevant items from each individual file.
'''


import json
import os
final_count = 0
final_json_data = []

path = os.path.join(os.getcwd(), "data/individual_tag_data")
# print(path)

file_name_list = os.listdir(path)
# remove unnecessary files
file_name_list = [i for i in file_name_list if i.endswith('.json')]
tag_list = [i[:len(i)-5] for i in file_name_list]

for file_name, tag in zip(file_name_list, tag_list):

    count = 0
    json_data = json.load(open(os.path.join(path,file_name)))

    # Check if posts are relevant by checking tags in title or tag
    for key in json_data:
        try:
            final_json_data.append(key)
            count += 1
            final_count += 1
        except Exception as e:
            print(str(e))

    print("Number of total post for ", tag, "is =", count)


# Output the updated file with pretty JSON
target_filename = "data/integrated_all_post_data_final.json"
open(os.path.join(os.getcwd(),target_filename), "w").write(
        json.dumps(final_json_data, sort_keys=True, indent=4, separators=(',', ': '))
    )

print("The number of total post is: ", final_count)
