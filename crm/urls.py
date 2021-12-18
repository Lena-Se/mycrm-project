from django.urls import path, include
from django.views.i18n import JavaScriptCatalog
from . import views


client_urlpatterns = [
    path('', views.ClientsListView.as_view(), name='clients'),
    path('details/<slug:slug>/', views.ClientDetailView.as_view(), name='client-details'),
    path('create/', views.ClientCreateView.as_view(), name='client-create'),
    path('update/<slug:slug>/', views.ClientUpdateView.as_view(), name='client-update'),
    path('delete/<slug:slug>/', views.ClientDeleteView.as_view(), name='client-delete'),
]

project_urlpatterns = [
    path('', views.ProjectsListView.as_view(), name='projects'),
    path('details/<int:pk>/', views.ProjectDetailView.as_view(), name='project-details'),
    path('create/<slug:client_slug>/', views.ProjectCreateView.as_view(), name='project-create'),
    path('update/<int:pk>/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('delete/<int:pk>/', views.ProjectDeleteView.as_view(), name='project-delete'),
]

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('clients/', include(client_urlpatterns)),
    path('projects/', include(project_urlpatterns)),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    # url(r'^ckeditor/', include('ckeditor_uploader.urls')),
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
