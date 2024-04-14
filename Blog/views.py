from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from Blog.models import Blogs, Comment, LogUser, Response_
from Blog.forms import UserLogForm, UserSignForm
from .ResponseModels import ResponseBlogs
from rest_framework.response import Response
from django.db.models import Count

def login(request):
    return Response({"Message":"its working"})
    if request.method == 'POST':
        form = UserLogForm(request.POST)
        if form.is_valid():
            Username = form.cleaned_data['username']
            Password = form.cleaned_data['password']
            try:
                obj  = LogUser.objects.get(username=Username.upper())
                if obj.username==Username.upper() and obj.password==Password:
                    request.session["username"] = Username.upper()
                    return render(request,'home.html',{'username':obj.username})
                elif obj.username.upper()==Username.upper():
                    messages.add_message(request,messages.ERROR,"Password is incorrect")
                    return render(request,'login.html',{'form':form})
            except:
                messages.add_message(request,messages.ERROR,"User not exist")
        else:
            return render(request,'login.html',{'form':form})
    form = UserLogForm()
    return render(request,'login.html',{'form':form})
def signup(request):
    if request.method=='POST':
        fm = UserSignForm(request.POST)
        if fm.is_valid():
            Un = fm.cleaned_data['username']
            Pwd = fm.cleaned_data['password']
            type = fm.cleaned_data['userType']
            try:
                obj = LogUser.objects.get(username=Un.upper())
                messages.add_message(request,messages.WARNING,"User already Exist with us")
            except:
                #val = User.objects.latest('id').id #aggregate(Max('id'))
                U1 = LogUser(username=Un.upper(),password=Pwd,userType = type)
                U1.save()
                return redirect('/')              
        else:
            return render(request,'signup.html',{'us':fm})
    else:
        fm = UserSignForm()
    return render(request,'signup.html',{'us':fm})
def homepage(request):
    return render(request,'home.html',{'username':'Guest'})
def ViewBlogs(request):
    blogname = ''
    comments = ''
    like = ''
    if request.method == 'POST' and "comments" in request.POST:
        username = request.session["username"]
        blogname = request.POST.get('blog')
        user = LogUser.objects.get(username = username)
        blog = Blogs.objects.get(name = blogname)
        comments = request.POST.get('comments')
        dtnow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c1 = Comment(blog=blog,user=user,comment_text = comments,created_date = dtnow,modified_date = dtnow)
        c1.save()
    elif request.method=='POST' and 'like' in request.POST:
        username = request.session["username"]
        blogname = request.POST.get('blog')
        user = LogUser.objects.get(username = username)
        blog = Blogs.objects.get(name = blogname)
        dtnow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        like ='Liked the blog'
        r1 = Response_(blog = blog,user = user, like_or_not = True,response_date = dtnow)
        r1.save()
    elif request.method=='POST' and 'dislike' in request.POST:
        username = request.session["username"]
        blogname = request.POST.get('blog')
        user = LogUser.objects.get(username = username)
        blog = Blogs.objects.get(name = blogname)
        dtnow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        like ='DisLiked the blog'
        r1 = Response_(blog = blog,user = user, like_or_not = False,response_date = dtnow)
        r1.save()
    obj = Blogs.objects.all()
    return render(request,'Blogs.html',{'blogs':obj,'blogname':blogname,'comment':comments,'like':like})                                  
def AddBlog(request):
    if request.method == 'POST' and 'blogname' in request.POST:
        blogname = request.POST.get('blogname')
        blogcontent = request.POST.get('blogcontent')
        username = request.session["username"]
        user = LogUser.objects.get(username = username)
        user.userType  = "Author" 
        u1 = LogUser(username = username,password = user.password,userType = user.userType)
        u1.save()
        dtnow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        b1 = Blogs(name = blogname,content = blogcontent,author = user,created_date = dtnow,modified_date = dtnow)
        b1.save()
        obj = Blogs.objects.all()
        return redirect('/ViewBlogs') 
    return render(request,'AddBlog.html')

def MyBlogs(request):
    username = request.session["username"]
    user = LogUser.objects.get(username = username)
    if user.userType.upper() == "READER":
        return HttpResponse("Hey! Seems you haven't posted any Blogs")
    objs = Blogs.objects.filter(author = user)
    lst = []
    for obj  in objs:
        comment1 = Comment.objects.filter(blog = obj)
        response1 = Response_.objects.filter(blog = obj)
        likes = len([res.like_or_not for res in response1 if res.like_or_not])
        dislike = len(response1)-likes
        r1 = ResponseBlogs(blog = obj,likes = likes,dislikes = dislike,comments = len(comment1))
        lst.append(r1)
    return render(request,'MyBlogs.html',{"blogs":lst})

def Top5Commented(request):
    
    username = request.session["username"]
    user = LogUser.objects.get(username = username)
    if user.userType.upper() == "READER":
        return HttpResponse("Hey! Seems you haven't posted any Blogs")
    objs = Blogs.objects.filter(author = user).annotate(comment_count = Count('comment')).order_by('-comment_count')[:5]
    return render(request,'Top5Commented.html',{"data":objs})

def Top5LikedAndDisLiked(request):
    username = request.session["username"]
    dat = datetime.now() - timedelta(days=3)
    user = LogUser.objects.get(username = username)
    if user.userType.upper() == "READER":
        return HttpResponse("Hey! Seems you haven't posted any Blogs")
    liked_objs = Blogs.objects.filter(author = user,created_date__gte=dat,response__like_or_not=True).annotate(like_count = Count('response')).order_by('-like_count')[:5]
    disliked_objs = Blogs.objects.filter(author = user,created_date__gte=dat,response__like_or_not=False).annotate(like_count = Count('response')).order_by('-like_count')[:5]
    return render(request,'Top5LikedAndDisLiked.html',{"liked":liked_objs,"disliked":disliked_objs})

def Recent5LikedBlogs(request):
    username = request.session["username"]
    user = LogUser.objects.get(username = username)
    objs = Response_.objects.filter(user= user,like_or_not = True).order_by('-response_date')[:5]
    return render(request,'Recent5LikedBlogs.html',{"data":objs})

def CommentHistory(request):
    username = request.session["username"]
    user = LogUser.objects.get(username = username)
    blogname = request.POST.get('blog')
    blog = Blogs.objects.get(name = blogname)
    objs = Comment.objects.filter(blog = blog,user = user)
    return render(request,'CommentHistory.html',{'data':objs})
    
def CommentHistoryOfParticularAuthor(request):
    if request.method == 'POST':
        username = request.session["username"]
        user = LogUser.objects.get(username = username)
        authorname = request.POST.get('author')
        author = LogUser.objects.get(username = authorname.upper())
        blogs = Blogs.objects.filter(author = author)
        comment = Comment.objects.filter(blog__in = blogs,user = user)
        return render(request,'CommentHistoryOfParticularAuthor.html', {'data':comment})
    return render(request,'CommentHistoryOfParticularAuthor.html')
    