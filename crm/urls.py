from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('clients/', views.ClientsListView.as_view(), name='clients'),
    path('clients/<slug:slug>', views.ClientDetailView.as_view(), name='client_detail'),
]