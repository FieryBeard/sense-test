from tortoise import Model, fields


class Article(Model):
    id = fields.UUIDField(pk=True)
    title = fields.TextField()
    preview = fields.TextField()
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    comments = fields.IntField(default=0)
    author = fields.TextField()

    class Meta:
        table = "articles"

    def __str__(self):
        return self.id
