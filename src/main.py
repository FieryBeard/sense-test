import settings
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import NotFound, MethodNotSupported
from tortoise.contrib.sanic import register_tortoise
from datetime import datetime, time, timedelta
from sanic_scheduler import SanicScheduler, task
from denver import DenverAPI
from models import Article
from api import api
from aiocache import caches

caches.set_config({
    'default': {
        'cache': "aiocache.RedisCache",
        'endpoint': "127.0.0.1",
        'port': 6379,
        'timeout': 1,
        'serializer': {
            'class': "aiocache.serializers.PickleSerializer"
        },
        'plugins': [
            {'class': "aiocache.plugins.HitMissRatioPlugin"},
            {'class': "aiocache.plugins.TimingPlugin"}
        ]
    }
})

app = Sanic(__name__)
scheduler = SanicScheduler(app)
app.blueprint(api)


@task(timedelta(minutes=10))
async def store_all_articles(_):
    print("Store all articles", datetime.now())

    async def get_all_articles(page):
        articles = DenverAPI().get_articles(page)
        print(articles['pagination'])
        await Article.bulk_create(
            objects=articles['result'],
            update_fields=['comments'],
            on_conflict=['id']
        )
        if page < articles['pagination']['total']:
            page += 1
            await get_all_articles(page)

    await get_all_articles(1)


@app.exception(MethodNotSupported)
async def method_not_supported(request, exception):
    return json({'type': 'error', 'message': 'Method not allowed'}, status=405)


@app.exception(NotFound)
async def not_found(request, exception):
    return json({'type': 'error', 'message': 'Page not found', 'code': 404}, status=404)

register_tortoise(
    app,
    db_url=f"postgres://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}",
    modules={"models": ["models.__init__"]},
    generate_schemas=True
)

if __name__ == '__main__':
    app.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT, debug=settings.DEBUG, workers=1)
