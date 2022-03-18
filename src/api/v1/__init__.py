from sanic import Blueprint
from .articles import bp as articles

v1 = Blueprint.group(articles, url_prefix="/v1")