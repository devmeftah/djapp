from django.urls import path
from . import views

urlpatterns = [
    path('addmonitor', views.addmonitor, name='addmonitor'),
    path('monitors', views.monitors, name='monitors'),
    path('addcar', views.addcar, name='addcar'),
    path('addsociete', views.addsociete, name='addsociete'),

    path('<int:mnt_id>', views.updatemonitor, name='updatemonitor'),
]