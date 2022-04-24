import re
import json


class PostDetais(object):
    def __init__(self, soup, link=None):
        self.page_soup = soup
        self.link = link
    
    # returns the basic JSON response
    # collection target -> title, author infos, publication dates, tags, post links etc
    def json_response_basic(self):
        try:
            for my_tag in self.page_soup.find_all('script', {
                'type': "application/ld+json"}):
                res = my_tag.text
                return res
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_response"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""
    
    # returns a larger json response with rigorous information
    # collection target -> read time, upvotes, responses etc
    def json_response_whole(self):
        try:
            # [source: https://stackoverflow.com/questions/13323976/how-to-extract-a-json-object-that-was-defined-in-a-html-page-javascript-block-us 
            # script = re.compile('window.__APOLLO_STATE__ = ({.*})', re.DOTALL)
            # json_text = script.search(str(self.page_soup)]
            # following code of mine looks simpler :D
            for tag in self.page_soup.find_all('script'):
                if 'window.__APOLLO_STATE__' in tag.text:
                    data = tag.text
            return data[26:]
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_response"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""
    
    # find particular first key that is required in the larger json response
    # we're using regex as post number will be different for each post
    # we know that the post key starts with "Post:"
    def find_first_key(self, json_data):
        find_key_string = [re.compile("^Post:*").match]
        required_key = [k for k,v in json_data.items()
                if any (item(k) for item in find_key_string)]
        return required_key[0]
    

    # return post title using h1 tag
    # it could be collected from the basic json response as well
    def get_title(self):
        try:
            for my_tag in self.page_soup.find_all('h1'):
                title = my_tag.text
                return title
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_title"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""
    
    # returns two values: name and url
    def get_author_name(self, json_data):
        try:
            author_name = json_data['author']['name']
            author_url = json_data['author']['url']
            return author_name, author_url
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_title"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""
    
    # return 3 dates for a post- creation, publication, & last modification date
    def get_date(self, json_data):
        try:
            creation_date = json_data['dateCreated']
            published_date = json_data['datePublished']
            last_modification_date = json_data['dateModified']
            return creation_date, published_date, last_modification_date
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_title"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""
    
    
    def get_tags(self, key, json_data):
        try:
            tags = []
            for item in json_data[key]['tags']:
                tags.append(item["__ref"][4:])
            return tags
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_tags"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def get_read(self, key, json_data):
        try:
            read = json_data[key]['readingTime']
            return read
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_title"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def get_upvote(self, key, json_data):
        try:
            clap_count = json_data[key]['clapCount']
            voter_count = json_data[key]['voterCount']
            return clap_count, voter_count
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_upvote"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""


    def get_post_content(self):
        try:
            # class_="section-content"
            # we are using <article> tag as section-content class no longer works
            # everything is inside the article tag including title & author names
            for content in self.page_soup.find_all('article'):
                return content.text
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_post_content"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""
    
    
    def get_response(self, key, json_data):
        try:
#             res = json_data[key]['responsesCount']
            res = json_data[key]['postResponses']
            return res["count"]
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_response"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""
    