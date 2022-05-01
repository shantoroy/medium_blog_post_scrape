import json


class PostDetais(object):
    def __init__(self, soup, link=None):
        self.page_soup = soup
        self.link = link

    def get_title(self):
        class_names = ['graf graf--h3 graf-after--figure graf--title',
                       'graf graf--h3 graf--leading graf--title',
                       'graf graf--h3 graf-after--figure graf--trailing graf--title']
        try:
            for my_tag in self.page_soup.find_all(True, {
                'class': class_names}):
                title = my_tag.text
                return title
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_title"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def get_author_name(self):
        class_names = "ds-link ds-link--styleSubtle ui-captionStrong u-inlineBlock link link--darken link--darker"
        try:
            for my_tag in self.page_soup.find_all(
                    class_=class_names):
                name = my_tag.text
                return name
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_title"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def get_date(self):
        class_names = 'time'
        try:
            for my_tag in self.page_soup.find_all(class_names):
                date_time = my_tag.text
                return date_time
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_title"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def get_read(self):
        try:
            for my_tag in self.page_soup.find_all(class_="readingTime"):
                read = my_tag.get('title')
                return read
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_title"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def get_upvote(self):
        class_names = 'u-relative u-background js-actionMultirecommendCount u-marginLeft5'
        try:
            for my_tag in self.page_soup.find_all('span', {
                'class': class_names}):
                upvotes = my_tag.text
                return upvotes
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_upvote"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def get_body(self):
        news_body = ""
        for paragraphs in self.page_soup.find_all(
                class_='graf graf--p graf-after--p'):
            news_body += paragraphs.text.rstrip().lstrip()
        return news_body

    def get_post_content(self):
        try:
            for content in self.page_soup.find_all(class_="section-content"):
                return content.text
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_post_content"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""

    def get_response(self):
        class_names = 'button button--chromeless u-baseColor--buttonNormal u-marginRight12'
        try:
            class_names = 'button button--chromeless u-baseColor--buttonNormal u-marginRight12'
            for my_tag in self.page_soup.find_all('button', {
                'class': class_names}):
                res = my_tag.text
                return res
        except Exception as e:
            error_trace = {}
            error_trace["link"] = self.link
            error_trace["method"] = "get_response"
            error_trace["message"] = str(e)
            print(json.dumps(error_trace, indent=4))
        return ""
