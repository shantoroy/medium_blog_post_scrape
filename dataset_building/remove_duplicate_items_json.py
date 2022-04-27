import json

with open("integrated_all_post_data_final.json", "r") as f:
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

with open("related_data_rm_duplicacy_final_conf.json", "w") as f:
    json.dump(listed_dictionary_items, f)
print("# of post after removing duplicacy = ", len(listed_dictionary_items))
