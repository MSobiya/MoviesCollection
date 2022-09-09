"""MoviesCollection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
import CollectionAPI.views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('request_count/', CollectionAPI.views.get_request_count, name='request_count'),
    path('request_count/reset/', CollectionAPI.views.reset_request_count, name='reset_request_count'),
    path('register/', CollectionAPI.views.register, name='register'),
    path('movies/', CollectionAPI.views.movies, name='movies'),
    path('collection/', CollectionAPI.views.collections, name='collections'),
    path('collection/<uuid:collection_uuid>/', CollectionAPI.views.collections, name='collections'),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
] 
