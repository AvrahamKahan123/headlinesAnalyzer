from src.headlines.ArticleHeadline import ArticleHeadline


class Viewer:

    def __init__(self):
        self.headline_A = ArticleHeadline(title="I love EJ's soups", source="AvrahamNews.com", id=3000)

    def print_json(self):
        self.headline_A.add_pnoun("EJ")
        self.headline_A.add_pnoun("Pizza") # this is not grammatically true
        print(self.headline_A.to_json())

    def print_tokens(self):
        print(self.headline_A.tokenized())

if __name__ == '__main__':
    viewer = Viewer()
    viewer.print_tokens()
    viewer.print_json()