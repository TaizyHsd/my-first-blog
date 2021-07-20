from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
]

"""
mysite/urls.pyで http://127.0.0.1:8000/ へのアクセスはすべて
blogへリダイレクトされるようになっている。
blog/urls.pyでは、リダイレクトをviews.post_listに指定している。
パスが / だけのURLをルートURLという。
"""