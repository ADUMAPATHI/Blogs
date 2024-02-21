from django.contrib import admin

from Blog.models import LogUser,Blogs,Comment,Response

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=["username"]
admin.site.register(LogUser,UserAdmin)
admin.site.register(Blogs)
admin.site.register(Comment)
admin.site.register(Response)