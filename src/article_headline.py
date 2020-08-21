import json
from datetime import datetime

class ArticleHeadline:

    def __init__(self, title: str, source: str, article_date = datetime.date(datetime.now()), article_time = datetime.time(datetime.now())):
        self.title = title.replace("\'", "\'\'")
        self.source = source
        self.article_date = article_date
        self.article_time = article_time


    def to_json(self):
        data_dict = {"title": self.title, "source": self.source, "atime": self.article_time, "adate": self.article_date}
        return json.dumps(data_dict)




