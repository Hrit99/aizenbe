from app import ma
from marshmallow import fields

class UrlSchema(ma.Schema):
    url = fields.Str(required=True)
