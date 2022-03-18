import requests
from schemas import DenverArticleSchema, DenverGetArticlesSchema


class DenverAPI():
    def request(self, method: str, path: str, params: dict = None):
        try:
            req = requests.request(method, 'http://denver.sensearena.com/api/v1/'+path, params=params)
            data = req.json()
            return data
        except:
            return None

    def get_articles(self, page=1):
        try:
            return DenverGetArticlesSchema().load(self.request('GET', 'articles', {'page': page}))
        except:
            return None

    def get_article_by_uuid(self, uuid):
        try:
            return DenverArticleSchema().load(self.request('GET', f'article/{uuid}'))
        except:
            return None


    def get_article_comments(self, uuid):
        return self.request('GET', f'article/{uuid}/comments')

