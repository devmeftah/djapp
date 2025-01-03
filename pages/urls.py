from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('search', views.search, name='search'),

    path('about', views.about, name='about'),    
]