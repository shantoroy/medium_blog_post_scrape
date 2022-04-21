import json
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

    file_name_list = ["smart-contracts.json"]
    tag_list = ["smart contract"]

    for file_name, tag in zip(file_name_list, tag_list):
        scrapper = MediumScrapper(tag, CHROME_DRIVER_PATH=CHROME_DRIVER_PATH)
        output_filename = file_name
        data = scrapper.get_post_contents()
        with open(output_filename, 'w') as fp:
            json.dump(data, fp)
        print("Check JSON file: {}".format(output_filename))
        print("Total posts: {}".format(len(data)))
