"""
This program integrates all the relevant posts from
JSON files for each keyword. We check relevancy by searching
the keyword either in title or in tag. The program also
prints the number of relevant items from each individual file.

Author : Shanto Roy
Year : 2019
"""

import json
final_count = 0
final_json_data = []

file_name_list = ["smart-contract.json", "smart-contracts.json", "metamask.json",
                      "solidity.json", "vyper.json",
                      "truffle.json", "web3.json", "erc20.json", "security.json"]
tag_list = ["smart contracts", "smart contract", "metamask", "solidity", "vyper",
                "smart contracts", "web3", "erc20", "security"]

for file_name, tag in zip(file_name_list, tag_list):

    count = 0
    json_data = json.load(open("post_data/"+file_name))

    # Check if posts are relevant by checking tags in title or tag
    for key in json_data:
        tags = key['tags']

        for item in tags:
            if tag in item.lower():
                final_json_data.append(key)
                count += 1
                final_count += 1
    print("Number of total post for ", tag, "is =", count)


# Output the updated file with pretty JSON
open("integrated_all_post_data_selective_without_truffle.json", "w").write(
        json.dumps(final_json_data, sort_keys=True, indent=4, separators=(',', ': '))
    )

print("The number of total post is: ", final_count)
