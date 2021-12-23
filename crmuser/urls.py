from django.contrib.auth.views import PasswordChangeView
from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.UserDetailView.as_view(), name='crmuser-cabinet'),
    path('profile/edit/', views.UserUpdateView.as_view(), name='crmuser-edit'),
    path('profile/change_password/', PasswordChangeView.as_view(), )

]
