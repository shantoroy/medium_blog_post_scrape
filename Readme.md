# Medium Post Scrape for Blog Dataset

## Initial Setup
* Download chromedriver
* Install Anaconda/ Miniconda (Recommended).
* Create/run in a python 3.6 virtual environment
* run `pip install -r requirements.txt`

## Medium Post Analysis
### Download Blog Posts
```Bash
$ cd post_data
$ python medium_post_scrapper_app.py
```

### Integrate all posts
```Bash
$ cd ..
$ python all_posts_integration.py
```

### Remove Duplicate posts
```Bash
$ python remove_duplicate_items_json.py
```

### Post Analysis
```Bash
$ python post_analysis.py
```

## Medium Author Information Analysisls
### Download related author data
```Bash
$ cd author data
$ python medium_author_scrapper.py
```


## N.B.
* Do not forget to download the `chromedriver` of the similar version as of the chrome browser
* Miniconda is recommended as it is very lightweight
