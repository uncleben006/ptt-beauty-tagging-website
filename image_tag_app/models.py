from djongo import models


# Create your models here.
class Comments(models.Model):
    status = models.CharField(max_length = 32)
    comment_id = models.CharField(max_length = 128)
    content = models.CharField(max_length = 512)
    ip = models.CharField(max_length = 128)
    comment_time = models.CharField(max_length = 128)

    class Meta:
        abstract = True

class Data(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length = 256)
    url = models.CharField(max_length = 512)
    slug = models.CharField(max_length = 256)
    post_time = models.CharField(max_length = 256)
    push = models.CharField(max_length = 8)
    imgs = models.JSONField()
    author = models.CharField(max_length = 256)
    comments = models.ArrayField(model_container = Comments)
    tags = models.JSONField()
    taggers = models.JSONField()
