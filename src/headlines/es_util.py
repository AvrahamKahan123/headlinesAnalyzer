from typing import List
from elasticsearch7 import Elasticsearch
from headlines.extract_topics import Topic


def get_es_client():
    return Elasticsearch({'host': 'localhost', 'port': 9200}, timeout=300)


def get_topic_request(topic: Topic):
    """ Creates indexing request body for ES for Topic object"""
    request = {
        'id': topic.id,
        'keywords': topic.keywords
    }
    return request


def index_topics(topics: List[Topic]) -> None:
    es_client = get_es_client()
    for topic in topics:
        request = get_topic_request(topic)
        es_client.index(index='topicsIndex', doc_type='topic', body=request) # id will be auto generated


