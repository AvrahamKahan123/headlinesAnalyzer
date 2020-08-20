import elasticsearch7
from elasticsearch7 import Elasticsearch
from article_headline import ArticleHeadline

class ElasticArticle:
    def __init__(self):
        self.es_connection = Elasticsearch([{'host': 'localhost', 'port': 9200}])


    def add_article(self, headline: ArticleHeadline):
        self.es_connection.index(index='aggregateheadlines', doc_type='headline', body=headline.to_json())

    def search_es(self, search_term: str):
        self.es_connection.search(index="aggregateheadlines", body={"query": {"match": {'title': {search_term}}}})
        

if __name__ == '__main__':
    pass



