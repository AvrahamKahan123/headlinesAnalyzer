import re
from headlines import article_headline

class AdvancedHeadline(article_headline.ArticleHeadline):


    def extract_people(self):
        words = re.split(self.title, "\s|")
        possible_names = self.combine_names([word for word in words])


    def combine_names(self, possible_names):
        filtered_names = []
        current_name = ""
        for name in possible_names:
            if len(name) == 1:
                pass
            elif bool(re.match(name, ",|'")) or (name[-2] == "'" and name[-1] == "s"):
                current_name += name
                filtered_names.append(current_name)
                current_name = ""
            elif name[0].islower():
                if (len(current_name) > 0)
                    filtered_names.append(current_name)
                current_name = ""
        return filtered_names



