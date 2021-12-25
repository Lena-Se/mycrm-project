"""mycrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from interactions import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crm.urls')),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

interactions_urlpatterns = [
    path('', views.InteractionsListView.as_view(), name='interactions'),
    path('details/<int:pk>/', views.InteractionDetailView.as_view(), name='interaction-details'),
    path('create/<int:project_id>', views.InteractionCreateView.as_view(), name='interaction-create'),
    path('update/<int:pk>/', views.InteractionUpdateView.as_view(), name='interaction-update'),
    path('delete/<int:pk>/', views.InteractionDeleteView.as_view(), name='interaction-delete'),
    path('add_mark/<int:pk>/', views.InteractionAddMarkRedirectView.as_view(), name='add-mark'),
]

# Add interactions urls
urlpatterns += [
    path('interactions/', include(interactions_urlpatterns)),
]

# Add crmuser urls
urlpatterns += [
    path('crmuser/', include('crmuser.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)