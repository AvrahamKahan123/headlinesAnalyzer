import spacy, json, re
from spacy.lang.en import stop_words
from collections import namedtuple
from typing import List, Callable
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem.snowball import SnowballStemmer
from headlines import webscraper
from headlines import psql_util


class ArticleHeadline:
    """ Represents headline scraped from the web. Contains id of Article in postgres, as well as extracted peoples, places, and organizations"""
    def __init__(self, title: str, source: str, id = -1,
                  proper_nouns = []):
        self.title = title
        self.source = source
        self.proper_nouns = proper_nouns
        self.id = id
        self.topic_index = -1 # topic its matched to
        self.max_propn_length = 4
        self.max_acronym_length = 5

    def create_insert_article(self) -> str:
        """ Returns insert statement for article """
        SQL_safe_title = self.title.replace("\'", "\'\'") # so does not cause SQL to think ' marks a string
        return f"INSERT into allheadlines(newsorg, title, articledate, articletime) values('{self.source}', '{SQL_safe_title}', CURRENT_DATE, CURRENT_TIME) ON CONFLICT DO NOTHING;"

    def to_json(self):
        data_dict = {"title": self.title, "source": self.source, "apnouns": self.proper_nouns}
        return json.dumps(data_dict)

    def cleaned(self):
        """ Method is here so as to provide mechanism to change way 'cleaned' title is generated in the future"""
        return self.tokenized().join(' ')

    def tokenized(self) -> List[str]:
        """ Extracts stemmed and cleaned tokens of title. May be used as part of the parsing"""
        tokens = self.tokenizer(self.title)
        cleaned_tokens = self.remove_stop_words(tokens)
        stemmed_tokens = self.stemmer(cleaned_tokens)
        final_tokens = self.remove_singlequotes(stemmed_tokens) #for some reason single quotes are not removed, unlike other punctuation
        return final_tokens

    def tokenizer(self, text):
        """ Tokenize title"""
        tokenizer = WhitespaceTokenizer()
        tokenized_list = tokenizer.tokenize(self.title)
        return tokenized_list

    def remove_stop_words(self, tokens):
        stopwords: set = spacy.lang.en.stop_words.STOP_WORDS
        cleaned_tokens = filter(lambda x: x not in stopwords, tokens)
        return cleaned_tokens


    def stemmer(self, tokens: List[str]):
        """ Stem tokenized title"""
        snowball = SnowballStemmer(language='english')
        stemmed_list = [snowball.stem(word) for word in tokens]
        return stemmed_list

    def remove_singlequotes(self, tokens):
        return [token.replace("'", "") for token in tokens]

    def get_all_pnouns(self):
        """ Returns list containing all proper nouns for this headline"""
        return self.proper_nouns

    def add_pnoun(self, p_noun):
        self.proper_nouns.append(p_noun)

    def __str__(self):
        return self.title


AbbrevReplacement = namedtuple("AbbrevReplacement", "abbrev full")
ProperNoun = namedtuple('ProperNoun', 'noun label') # basically a small container class with fields noun and label
SearchHit = namedtuple('search_hit', 'id type search_term')


class HeadlineParser():
    """ Provides functionality to discover names, places, and other proper nouns mentioned in headline """
    def __init___(self, headline: ArticleHeadline, connection = psql_util.get_db_connection()):
        self.headline = headline
        self.connection = connection
        self.max_propn_length = 4
        self.max_acronym_length = 5

    def parse(self) -> None:
        """ Extacts names, places, etc. and stores them to the places variable """
        interpreted_headline = self.interpret_abbreiviations()
        proper_nouns: List[ProperNoun] = self.get_all_proper(interpreted_headline)
        for candidate in proper_nouns:
            self.parse_candidate(candidate)

    def intepret_abbreviations(self) -> str:
        """
        :returns string with abbreviations replaced with their full names
        Will use abbreivations table to understand abbreviations in headline and set that as new headline. Ex. 'Conn.' -> 'Connecticut'
        Doesn't add directly to proper Nouns since abbreviation may be part of larger proper noun """
        title_copy = self.title # in python, strings are primitives; the value is copied
        tokens = title_copy.split(" ")
        candidate_abreviations = [token for token in tokens if token.endswith(".") and 2<=len(token)<=5]
        abbrev_replacements: List[AbbrevReplacement] = []
        for abbreviation in candidate_abreviations:
            full_abbrev = self.query_abbreviation(abbreviation)
            if full_abbrev:
                abbrev_replacements.append(AbbrevReplacement(abbrev=abbreviation, full=full_abbrev))
        for replacement in abbrev_replacements:
            title_copy.replace(replacement.abbrev, replacement.full)
        return title_copy

    def query_abbreivation(self, abbreviation: str) -> str:
        query = f"SELECT fullName from Abbreviations where abbreviation = '{abbreviation}'"
        result = psql_util.query_single_field(query, self.connection)
        if result:
            return result

    def get_all_proper(self, headline: str) -> List[ProperNoun]:
        """ Get list of all wanted (ie. of a useful type that we might want to track) proper nouns using spaCy"""
        nl_processor = spacy.load("en_core_web_sm")  # ISSUE: CANNOT RESOLVE LINK
        analyzed_title = nl_processor(headline)
        tracked_labels = ["PERSON", "NORP", "FAC", "ORG", "GPE"] # only nouns indentified as of this type will be returned
        return [ProperNoun(ent.text_, ent.label_) for ent in analyzed_title.ents if ent.label_ in tracked_labels] # ent returns only entities (ie. proper nouns)

    def parse_candidate(self, candidate: ProperNoun) -> None:
        """
        prime candidate to become threaded, since very little processing and long wait time on IO from the database
        Parses a single word and if it finds a hit, notes it in the db, etc
        Code must be added to remove punctuation and if need be, lemmatize the word"""
        #each search has its own function
        search_functions: List[Callable[[str], SearchHit]] = [self.search_NORP, self.search_acronym,
                                                              self.search_nicknames, self.search_pnouns, self.scrape_name()]
        for i in range(len(search_functions)):
            hit: SearchHit = search_functions[i](candidate)
            if hit:
                self.note_hit(hit)
                return
        hit = self.resolve_name(candidate)
        if hit:
            self.note_hit(hit)

    def search_norp(self, candidate: ProperNoun) -> SearchHit:
        if candidate.type != "NORP": # NORPs are easy to find, so we can rely on spaCy getting it right with them, unlike other labels
            return None
        query = f"SELECT id FROM Norps WHERE shortName = '{candidate.noun}'"
        search_id = psql_util.query_single_field(query, self.connection)
        if id:
            return SearchHit(search_id, "PLACE", candidate.noun)
        # else will return None

    def search_acronym(self, candidate: ProperNoun) -> SearchHit:
        if candidate.noun.count(" ") < 2 and re.match(f"[A-Z0-9]{2, {self.max_acronym_length}}", candidate.noun): # if is candidate to be acronym
            query = f"SELECT Acronym.id, ProperNoun.type FROM Acronyms INNER JOIN ON ProperNouns WHERE Acronyms.id = ProperNouns.id AND acronym = '{candidate.noun}'"
            search = psql_util.query_full_row(query, self.connection)
            if search:
                return SearchHit(search[0], search[1], candidate.noun)

    def search_nicknames(self, candidate: ProperNoun) -> SearchHit:
        query = f"SELECT Nicknames.id, ProperNouns.type FROM Nicknames INNER JOIN ON ProperNouns where Nicknames.id = ProperNouns.id  AND nickname = '{candidate.noun}'" # needs to be replaced by join
        search = psql_util.query_full_row(query, self.connection)
        if search:
            return SearchHit(search[0], search[1], candidate.noun)

    def search_pnouns(self, candidate):
        query = f"SELECT id, type FROM properNouns WHERE fullName = '{candidate.noun}'"
        search = psql_util.query_full_row(query, self.connection)
        if search:
            return SearchHit(search[0], search[1], candidate.noun)

    def note_hit(self, hit: SearchHit):
        psql_util.link_headline_pnoun(self.id, hit.id)
        self.headline.add_pnoun(hit.search_term)

    def resolve_name(self, candidate: ProperNoun):
        """ Resolves unidentified name using webscraping"""
        name = self.scrape_name(candidate.noun)
        if name: # needs explicit check to make sure double inserts of names don't happen, though this is unlikely in the extreme as per the current program flow
            newname_id = self.commit_name()
            return SearchHit(newname_id, "PERSON", name)
        else:
            return None

    def scrape_name(self, name: str):
        """ Scrapes full name off web given nickname or partial name"""
        full_name = webscraper.get_full_name(name)
        if full_name:
            name_corrected = full_name.replace('_', ' ')
            return name_corrected
        else:
            return None

    def commit_name(self, name) -> int:
        """
        This will be moved to new class soon since it violates SRP
        Commits new name to DB and gets its ID
        """
        insert_stmt = f"INSERT INTO ProperNouns(fullName, type) Values('{name}', 'PERSON') ON Conflict DO Nothing"
        psql_util.execute_insert(insert_stmt)
        query = f"SELECT ID FROM ProperNouns where fullName = '{name}'"
        id = psql_util.query_single_field(query, self.connection)
        return id



