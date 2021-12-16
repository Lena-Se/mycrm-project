from django.conf.urls import url
from django.urls import path, include
from . import views


client_urlpatterns = [
    path('', views.ClientsListView.as_view(), name='clients'),
    path('details/<slug:slug>/', views.ClientDetailView.as_view(), name='client-details'),
    path('create/', views.ClientCreateView.as_view(), name='client-create'),
    path('update/<slug:slug>/', views.ClientUpdateView.as_view(), name='client-update'),
]

project_urlpatterns = [
    path('', views.ProjectsListView.as_view(), name='projects'),
    path('details/<int:pk>/', views.ProjectDetailView.as_view(), name='project-details'),
    path('create/<slug:client_slug>/', views.ProjectCreateView.as_view(), name='project-create'),
    path('update/<slug:client_slug>/<int:pk>/', views.ProjectUpdateView.as_view(), name='project-update'),
]

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('clients/', include(client_urlpatterns)),
    path('projects/', include(project_urlpatterns)),
]

# urlpatterns = [
#     path('', views.IndexTemplateView.as_view(), name='index'),
#     path('clients/', views.ClientsListView.as_view(), name='clients'),
#     path('clients/details/<slug:slug>/', views.ClientDetailView.as_view(), name='client-details'),
#     path('clients/create/', views.ClientCreateView.as_view(), name='client-create'),
#     path('clients/update/<slug:slug>/', views.ClientUpdateView.as_view(), name='client-update'),
#     path('projects/', views.ProjectsListView.as_view(), name='projects'),
#     path('projects/details/<int:pk>/', views.ProjectDetailView.as_view(), name='project-details'),
#     path('projects/create/<slug:client_slug>/<int:pk>/', views.ProjectCreateView.as_view(), name='project-create'),
#     path('projects/update/<slug:client_slug>/<int:pk>/', views.ProjectUpdateView.as_view(), name='project-update'),
# ]
