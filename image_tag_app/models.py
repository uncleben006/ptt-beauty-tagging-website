from djongo import models


# Create your models here.

class Data(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length = 256)
    url = models.CharField(max_length = 512)
    slug = models.CharField(max_length = 256)
    post_time = models.CharField(max_length = 256)
    push = models.CharField(max_length = 8)
    imgs = models.JSONField()
    author = models.CharField(max_length = 256)
    comments = models.JSONField()
    tags = models.JSONField()
    tags_average = models.JSONField(default = {})
    taggers = models.JSONField()

    def __str__(self):
        return self.title + ' | ' + self.author + ' | ' + self.post_time + ' | ' + self.slug + ')'
