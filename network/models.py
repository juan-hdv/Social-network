from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	# A user likes several posts (likes) / A Post is liked by several users (fans)
	likes = models.ManyToManyField('Post',related_name="fans") # Likes & fans
	# A user follows other users / A user is followed by other users
	follows = models.ManyToManyField('self',symmetrical=False,related_name="followers")

	def __str__(self):
		return f"{self.username} ({self.email}) likes({self.likes.count()}) follows({self.follows.count()})"


class Post(models.Model):
# A Post is posted by a user in a datetime with given content
	author = models.ForeignKey(User, on_delete=models.CASCADE) # One User relates to Many Posts
	datetime = models.DateTimeField(auto_now=False, auto_now_add=True) # default=timezone.now
	content = models.CharField(max_length=280) # Like twitter length
	totallikes = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.datetime} <{self.author.username}> [{self.content}] Likes({self.totallikes}) fans({self.fans.count()})"

