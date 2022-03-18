from marshmallow import Schema, fields, post_load
from models import Article


class ArticleSchema(Schema):
    id = fields.UUID(required=True)
    title = fields.Str(required=True)
    preview = fields.Str()
    content = fields.Str()
    created_at = fields.DateTime(format='%d.%m.%Y %H:%M:%S', required=True)
    comments = fields.Integer(required=True)
    author = fields.Str()
