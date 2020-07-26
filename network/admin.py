from django.contrib import admin

# Register your models here.
from .models import User, Follower, Post

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follower)
