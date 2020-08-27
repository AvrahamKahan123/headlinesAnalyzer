import pandas as pd
from datetime import datetime
from sklearn.cluster import MiniBatchKMeans
from commit_headlinesDB import database_connector
from sklearn.feature_extraction.text import TfidfVectorizer
from headlines import advanced_headline


def get_articles(dt: datetime):
    """ Will query postgres for articles since given datetime"""
    pass

def convert_to_panda():
    """ convert all articles to panda"""

def extract_features(headlines: List[advanced_headline]) -> list:
    """ Will extract feature vectors for every given headline"""
    pass

def cluster(headline_features: list) -> List[Cluster]:
    """ Will use Scikit k means clustering to extract clusters"""


