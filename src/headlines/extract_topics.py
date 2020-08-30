from typing import List
from sklearn.pipeline import Pipeline
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import unicodedata, spacy
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.stem import WordNetLemmatizer
from headlines.ArticleHeadline import ArticleHeadline


class Topic:
    """ Represents topics extracted using NDA"""
    def __init__(self, id: int, keywords: List[str]):
        self.id = id
        self.keywords = keywords
        self.headlines = set()

    def add_headline(self, headline: ArticleHeadline):
        self.headlines.add(headline)


class TitleNormalizer(BaseEstimator, TransformerMixin):
    """ Normalizes title by lemmatizing the title and removing punctuations and stopwords"""
    def __init__(self, language='english'):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(spacy.spacy.lang.en.stop_words.STOP_WORDS) # set to allow faster search. spaCy used instead of NLTK stopwords since spaCy's are more completee

    def is_punct(self, token) -> bool:
        return all(
            unicodedata.category(char).startswith('P') for char in token
        )

    def is_stopword(self, token) -> bool:
        return token.lower() in self.stop_words


class FindTopics:
    """ Uses Latent Dirichlet Allocation to extract topics from a list of headlines"""
    def __init__(self, max_topics=10):
        """ N_topics is max number of expected topics"""
        self.max_topics = max_topics
        self.lda_model = Pipeline([('norm', TitleNormalizer()),
                                    # vectorizer should not convert title words to lowercase and should use only words of length >= 2
                                   ('vect', CountVectorizer(lowercase=False, token_pattern='[a-zA-Z0-9]{2,}')),
                                   ('model', LatentDirichletAllocation(n_topics=self.max_topics)),
                                   ])

    def fit_transform(self, documents):
        """ Calls fit_transform for every stage in the pipeline"""
        self.lda_model.fit_transform(documents)
        return self.lda_model

    def extract_topics(self, top_keywords=10) -> List[Topic]:
        vectorizer = self.lda_model.named_steps['vect']
        model = self.lda_model.steps[-1][1]
        keywords = vectorizer.get_feature_names()
        # topics is list of Topic objects extracted by NDA
        topics  = [Topic(index, [keywords[keyword_index] for keyword_index in topic.argsort()[:-(top_keywords - 1): -1]]) for index, topic in enumerate(model.components_)]
        return topics

