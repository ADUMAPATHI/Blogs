from django.db import models

# Create your models here.
class LogUser(models.Model):
    username = models.CharField(primary_key=True,max_length=50)
    password = models.CharField(max_length=50)
    userType = models.CharField(max_length=50)

class Blogs(models.Model):
    name          = models.CharField(primary_key=True,max_length = 40)
    content       = models.TextField()
    author        = models.ForeignKey(LogUser,on_delete = models.CASCADE)
    created_date  = models.DateTimeField()
    modified_date = models.DateTimeField()

class Comment(models.Model):
    blog           = models.ForeignKey(Blogs,on_delete = models.CASCADE)
    user           = models.ForeignKey(LogUser,on_delete = models.CASCADE)
    comment_text   = models.TextField()
    created_date   = models.DateTimeField()
    modified_date  = models.DateTimeField()

class Response_(models.Model):
    blog           = models.ForeignKey(Blogs,on_delete = models.CASCADE)
    user           = models.ForeignKey(LogUser,on_delete = models.CASCADE)
    like_or_not    = models.BooleanField()
    response_date  = models.DateTimeField()