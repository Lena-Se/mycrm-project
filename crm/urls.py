from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('clients/', views.ClientsListView.as_view(), name='clients'),
    path('clients/details/<slug:slug>', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/create', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/update/<slug:slug>', views.ClientUpdateView.as_view(), name='client_update'),
]