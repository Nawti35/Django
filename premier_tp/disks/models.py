from django.db import models

# Create your models here.
class album(models.Model):

    Title = models.CharField(max_length=160)
    artist = models.ForeignKey('artist', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "album"

    def __str__(self):
        return self.Title

class artist(models.Model):

    Name = models.CharField(max_length=120)

    class Meta:
        verbose_name = "artist"

    def __str__(self):
        return self.Name

class track(models.Model):

    Name = models.CharField(max_length=200)
    Composer = models.CharField(max_length=220)
    Milliseconds = models.TextField()
    Bytes = models.IntegerField()
    UnitPrice = models.DecimalField(decimal_places= 2,max_digits= 10)

    album = models.ForeignKey('album', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "track"

    def __str__(self):
        return self.Name