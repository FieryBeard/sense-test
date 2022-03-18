from marshmallow import Schema, fields, post_load
from .ArticleSchema import ArticleSchema
from .DenverAuthorSchema import DenverAuthorSchema
from models import Article


class DenverArticleSchema(ArticleSchema):
    author = fields.Nested(DenverAuthorSchema, dump_default=[])

    @post_load
    def make_article(self, data, **kwargs):
        data['author'] = f"{data['author']['first_name']} {data['author']['last_name']}"
        return Article(**data)

