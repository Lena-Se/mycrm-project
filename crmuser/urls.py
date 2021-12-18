from django.urls import path, include
from . import views

urlpatterns = [
    path('crmuser/<str:name>/', views.IndexTemplateView.as_view(), name='crmuser-cabinet'),
    path('crmuser/edit/<str:name>/', views.IndexTemplateView.as_view(), name='crmuser-edit'),

]
