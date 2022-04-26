import json
import os, errno
from medium_post_scrapper import MediumScrapper
try:
    from local_settings import *
except FileNotFoundError as fx:
    print(str(fx))


if __name__ == '__main__':
    global_tag_list = []

    # file_name_list = ["truffle.json", "web3.json", "etherscan.json",
    #                   "solidity.json", "reentrancy.json", "ethereum.json", "metamask.json",
    #                   "erc20.json", "vyper.json", "myetherwallet.json", "security.json"]
    # tag_list = ["truffle", "web3", "etherscan", "solidity", "reentrancy",
    #             "ethereum", "metamask", "erc20", "vyper", "myetherwallet", "smart contract security"]

    file_name_list = ["metamask.json"]
    tag_list = ["metamask"]

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
        scrapper = MediumScrapper(tag, CHROME_DRIVER_PATH=CHROME_DRIVER_PATH)
        output_filename = os.path.join(data_target_dir, file_name)
        data = scrapper.get_post_contents()
        with open(output_filename, 'w') as fp:
            json.dump(data, fp)
        
        print("")
        print("==========================================")
        print("Check JSON file: {}".format(output_filename))
        print("Total posts: {}".format(len(data)))

        # print tags for now
        # will be useful if you really want to apply real snowball effect
        # by collecting tags continuously from each post, store in a global tag list
        # and run scrapper for each tag that hasn't been visited before (use another list for visited)
        # currently not using it

        with open('tags.txt') as f:
            tag_list_snowball = [line.rstrip('\n') for line in f]
            for i in tag_list_snowball:
                global_tag_list.append(i)
        print("Tag List:", tag_list_snowball)
