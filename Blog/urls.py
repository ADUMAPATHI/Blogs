
from django.contrib import admin
from django.urls import path
from Blog import views

urlpatterns = [
    path('',views.login,name='login'),
    path('homepage',views.homepage,name='homepage'),
    path('signup/',views.signup,name='signup'),
    path('ViewBlogs/',views.ViewBlogs,name='ViewBlogs'),
    path('ViewBlogs/AddBlog/',views.AddBlog,name='AddBlog'),
    path('MyBlogs/',views.MyBlogs,name='MyBlogs'),
    path('Top5Commented/',views.Top5Commented,name='Top5Commented'),
    path('Top5LikedAndDisLiked/',views.Top5LikedAndDisLiked,name='Top5LikedAndDisLiked'),
    path('Recent5LikedBlogs/',views.Recent5LikedBlogs,name='Recent5LikedBlogs'),
    path('ViewBlogs/History/',views.CommentHistory,name='CommentHistory'),
    path('CommentHistoryOfParticularAuthor/',views.CommentHistoryOfParticularAuthor,name='CommentHistoryOfParticularAuthor'),

]

