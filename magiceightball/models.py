from djongo import models
from django_mongodb_engine.contrib import MongoDBManager


class MotionPicture(models.Model):
    tconst = models.TextField()
    rating = models.FloatField()
    votes = models.BigIntegerField()
    type = models.TextField()
    title = models.TextField()
    year = models.IntegerField()
    runtime = models.IntegerField()
    genres = models.TextField()
    
    objects = MongoDBManager()
    
    class Meta:
        db_table = 'motionPictures'
