from django.contrib import admin
from news.models import Blog, Comment, Contact
# Register your models here.

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Contact)