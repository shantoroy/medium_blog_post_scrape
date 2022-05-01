import json
from medium_post_scrapper import MediumScrapper
try:
    from local_settings import *
except FileNotFoundError as fx:
    print(str(fx))


if __name__ == '__main__':
    scrapper = MediumScrapper(CHROME_DRIVER_PATH=CHROME_DRIVER_PATH)
    output_filename = 'ripple.json'
    data = scrapper.get_post_contents()
    with open(output_filename, 'w') as fp:
        json.dump(data, fp)
    print("Check JSON file: {}".format(output_filename))
    print("Total posts: {}".format(len(data)))
