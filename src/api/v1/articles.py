from sanic import Blueprint, response
from models import Article
from schemas import ArticleSchema, DenverArticleSchema
from aiocache import caches
from datetime import datetime


bp = Blueprint("api_v1_articles", url_prefix="articles")


@bp.route('/')
async def get_articles(request):
    from_db = False
    start = datetime.now()
    cache = caches.get('default')
    articles = await cache.get(f'articles')
    if not articles:
        articles = await Article.all()
        articles = [ArticleSchema().dumps(article) for article in articles]
        from_db = True
        await cache.set(f'articles', articles, ttl=60)
    return response.json({"articles": articles, 'from_db': from_db, 'time': str(datetime.now() - start)})


@bp.route('/<article_id:uuid>')
async def get_article_by_uuid(request, article_id):
    from_db = False
    start = datetime.now()
    cache = caches.get('default')
    article = await cache.get(f'article:{article_id}')
    if not article:
        article = ArticleSchema().dumps(await Article.filter(id=article_id).first())
        from_db = True
        await cache.set(f'article:{article_id}', article, ttl=60)
    return response.json({'article': article, 'from_db': from_db, 'time': str(datetime.now() - start)})
