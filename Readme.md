# Medium Post Scrape for Blog Dataset (Under Development)

## Initial Setup
* Download chromedriver
* Install Anaconda/ Miniconda (Recommended).
* Create/run in a python >v3.6 virtual environment
* run `pip install -r requirements.txt`

## Medium Post Analysis
### Download Blog Posts
First add tags and related file names. Then do the following.
```Bash
$ cd scrapping/scripts/v.Apr.2022/
$ python main.py
```

### Integrate all posts
```Bash
$ cd dataset_building
$ python all_posts_integration.py
```

### Remove Duplicate posts
```Bash
$ cd dataset_building
$ python remove_duplicate_items_json.py
```

### Post Analysis
```Bash
$ cd analysis/scripts
$ python post_analysis.py
```

<!-- ## Medium Author Information Analysisls
### Download related author data
```Bash
$ cd author_data
$ python medium_author_scrapper.py
``` -->


## N.B.
* Do not forget to download the `chromedriver` of the similar version as of the chrome browser
* Miniconda is recommended as it is very lightweight
