from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.clients, name='clients'),

    path('addclient', views.addclient, name='addclient'),

    path('controle/<int:clt_id>', views.controle, name='controle'),

    path('<int:clt_id>', views.updateclient, name='updateclient'),
    path('paiement/<int:clt_id>', views.paiement, name='paiement'),
    
    path('contractpdf/<int:pk>', views.contractpdf, name='contractpdf'),
    path('certifiedpdf/<int:pk>', views.certifiedpdf, name='certifiedpdf'),
    path('paiementpdf/<int:pk>', views.paiementpdf, name='paiementpdf'),
    path('statistic', views.statistic, name='statistic'),
]