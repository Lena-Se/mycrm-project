from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('clients/', views.ClientsListView.as_view(), name='clients'),
    path('client/details/<slug:slug>', views.ClientDetailView.as_view(), name='client-details'),
    path('client/create/', views.ClientCreateView.as_view(), name='client-create'),
    path('client/update/<slug:slug>', views.ClientUpdateView.as_view(), name='client-update'),
]
