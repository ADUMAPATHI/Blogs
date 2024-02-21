from typing import Any
from django.db import models

from .models import Blogs
class ResponseBlogs(models.Model):
    blog : Blogs
    likes = models.IntegerField()
    dilikes = models.IntegerField()
    comments = models.IntegerField()
    def __init__(self, *args: Any,blog,likes,dislikes,comments) -> None:
        super().__init__(*args)
        self.blog = blog
        self.likes = likes
        self.dislikes = dislikes
        self.comments = comments