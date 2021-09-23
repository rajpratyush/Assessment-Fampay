from django.db import models


class YoutubeVideoModel(models.Model):

    video_title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    video_url = models.CharField(max_length=1000)
    video_id = models.CharField(max_length=1000)
    published_date = models.CharField(max_length=1000)



