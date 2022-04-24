import json
import os
from medium_post_scrapper import MediumScrapper
try:
    from local_settings import *
except FileNotFoundError as fx:
    print(str(fx))


if __name__ == '__main__':
    # file_name_list = ["truffle.json", "web3.json", "etherscan.json",
    #                   "solidity.json", "reentrancy.json", "ethereum.json", "metamask.json",
    #                   "erc20.json", "vyper.json", "myetherwallet.json", "security.json"]
    # tag_list = ["truffle", "web3", "etherscan", "solidity", "reentrancy",
    #             "ethereum", "metamask", "erc20", "vyper", "myetherwallet", "smart contract security"]

    file_name_list = ["metamask.json"]
    tag_list = ["metamask"]

    for file_name, tag in zip(file_name_list, tag_list):
        scrapper = MediumScrapper(tag, CHROME_DRIVER_PATH=CHROME_DRIVER_PATH)
        output_filename = os.path.join("../../data", file_name)
        data = scrapper.get_post_contents()
        with open(output_filename, 'w') as fp:
            json.dump(data, fp)
        
        print("")
        print("==========================================")
        print("Check JSON file: {}".format(output_filename))
        print("Total posts: {}".format(len(data)))

        # print tags
        with open('tags.txt') as f:
            tag_list_snowball = [line.rstrip('\n') for line in f]
        print("Tag List:", tag_list_snowball)
