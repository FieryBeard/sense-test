from marshmallow import Schema, fields
from .DenverArticleSchema import DenverArticleSchema


class DenverGetArticlesSchema(Schema):
    message = fields.Str()
    result = fields.List(fields.Nested(DenverArticleSchema))
    pagination = fields.Dict(keys=fields.Str(), values=fields.Int(), required=True)