from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class ServerRequest(models.Model):
	request_count = models.IntegerField()



class Movies(models.Model):
	uuid = models.CharField(max_length=40, primary_key=True)
	description = models.TextField()
	genres = models.TextField()
	title = models.CharField(max_length=1000)


class Collection(models.Model):
	collection_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE,)
	movies = models.ManyToManyField(Movies)
	title = models.CharField(max_length=1000)
	description = models.TextField()