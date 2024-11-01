from django.db import models

# Create your models here.
class Track(models.Model):
    title = models.CharField(max_length=250)
    artist = models.CharField(max_length=250)
    # description = models.TextField(blank=True)
    duration = models.FloatField()
    last_play = models.DateTimeField(null=True)
    # url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title