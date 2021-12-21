from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.UserDetailView.as_view(), name='crmuser-cabinet'),
    path('profile/edit/', views.UserUpdateVieww.as_view(), name='crmuser-edit'),

]
