from django.db import models

class Tracks(models.Model):
    artist_name = models.CharField(max_length=100)
    track_id = models.CharField(max_length=100)
    track_name = models.CharField(max_length=100)

    def __str__(self):
        return self.artist_name
