from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/<str:name>/', views.IndexTemplateView.as_view(), name='registration-cabinet'),
    path('registration/edit/<str:name>/', views.IndexTemplateView.as_view(), name='registration-edit'),

]
