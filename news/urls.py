from django.urls import path
from news.views import *
urlpatterns = [
    path('', homepage, name = 'homepage'),
    path('news', news, name = 'news'),
    path('welcome/<str:name>', welcome, name = 'greething'),
    path('blogs', blogs, name = 'blogs'),
    path('read/<str:id>', read, name = "read"),
    path('delete/<str:id>', delete , name = 'delete'),
    path('create', create, name = 'create'),
    path('edit/<str:id>', edit, name = "edit"),
    path('signup', signup, name= "signup"),
    path("login", login, name = 'login'),
    path("logout", logout, name='logout')
] 