from django.urls import path, include
from . import views

urlpatterns = [
    path('/<str:name>/', views.IndexTemplateView.as_view(), name='crmuser-cabinet'),
    path('/edit/<str:name>/', views.IndexTemplateView.as_view(), name='crmuser-edit'),

]
