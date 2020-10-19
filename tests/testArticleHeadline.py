import unittest
from src.headlines.ArticleHeadline import ArticleHeadline


class TestArticleHeadline(unittest.TestCase):
    def setUp(self):
        self.headline_A = ArticleHeadline(title="I love, EJ.'s soups?", source="AvrahamNews.com", id=3000)
        self.headline_A.add_pnoun("EJ")
        self.headline_A.add_pnoun("Pizza")  # this is not grammatically true

    def test_create_insert(self):
        self.assertEqual(self.headline_A.create_insert(),
                         "INSERT into allheadlines(newsorg, title, articledate, articletime) values('AvrahamNews.com', 'I love EJ''s soups', CURRENT_DATE, CURRENT_TIME) ON CONFLICT DO NOTHING;",
                         "create insert failed to create proper insert statement")

    def test_tokens(self):
        self.assertGreater(len(self.headline_A.tokenized()), 2)


if __name__ == '__main__':
    unittest.main()
