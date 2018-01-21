from django.db import models
from django.contrib.auth.models import Permission, User
# Create your models here.
class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    album_title = models.CharField(max_length=250)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title

class Picture(models.Model):
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    pic_title = models.CharField(max_length=250)
    pic_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.pic_title
