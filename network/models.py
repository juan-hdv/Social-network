from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
# A user likes several posts / A Post is liked by several users
	likes = models.ManyToManyField('Post') # Likes
	def __str__(self):
		return f"{self.username} ({self.email})"

class Post(models.Model):
# A Post is posted by a user in a datetime with given content
	author = models.ForeignKey(User, on_delete=models.CASCADE) # One User relates to Many Posts
	datetime = models.DateTimeField(auto_now=True, auto_now_add=False) # default=timezone.now
	content = models.CharField(max_length=280) # Like twitter length
	totallikes = models.IntegerField(default=0)
	def __str__(self):
		return f"{self.datetime} ({self.totallikes}) [{self.content}]"

class Follower(models.Model):
# A user is follower of another user
	user = models.ManyToManyField(User)
	def __str__(self):
		return f"Follower"
