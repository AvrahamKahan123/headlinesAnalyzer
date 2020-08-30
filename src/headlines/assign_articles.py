from typing import List
from headlines.ArticleHeadline import ArticleHeadline
from headlines.es_util import get_es_client


class ArticleAssigner:
    """ Discovers Topic to which ArticleHeadline objects belong to using ElasticSearch"""
    def __init__(self, headlines: List[ArticleHeadline], threshold: float):
        self.headlines = headlines
        self.threshold = threshold # threshold for ElasticSearch hit for a topic must be to be considered signifigant
        self.es_instance = get_es_client()

    def assign_articles(self):
        for head_line in self.headlines:
            search_results = filter(lambda hit: hit['_score'] > self.threshold, self.search_headline())
            if len(search_results == 0):
                search_results = filter(lambda hit: hit['_score'] > self.threshold, self.search_pnouns_headline())
                if len(search_results) == 0:
                    continue
            head_line.topic_index = search_results[0]['ident'] # this line will be changed later so that topic asisignment is based on more than ES search score

    def search_headline(self, head_line: ArticleHeadline):
        search_results = self.es_instance.search(index='topicsIndex', doc_type='topic', body={
            'query': {
                'match': {
                    "keywords": f"{head_line.cleaned()}"
                }
            }
        })
        return search_results

    def search_pnouns_headline(self, head_line: ArticleHeadline):
        search_results = self.es_instance.search(index='topicsIndex', doc_type='topic', body={
            'query': {
                'match': {
                    "keywords": f"{head_line.get_all_pnouns().join(' ')}"
                }
            }
        })
        return search_results






