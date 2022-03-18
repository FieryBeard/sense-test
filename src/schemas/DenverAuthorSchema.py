from marshmallow import Schema, fields


class DenverAuthorSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()

