from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'indexsdfssdfsdfef/',views.index,name='index'),
    url(r'login/',views.login),
    url(r'home/',views.Home.as_view()),
    #url(r'detail/',views.detail),
    url(r'detail-(\d+).html',views.detail),
    #url(r'detail-(?P<nid>\d+)-(?P<uid>\d+).html',views.detail),   #URL分组，指定view是参数为默认参数
]
