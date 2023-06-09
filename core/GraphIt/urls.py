"""
URL configuration for Graphlt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('load_data/<str:id>', views.load_data, name='data_plugin'),
    path('displayGraph/<str:id>', views.display_graph, name='view_plugin'),
    path('search/<str:search_param>', views.search, name='search'),
    path('filter/<str:search_param>', views.filter, name='filter'),
    path('complete_graph', views.complete_graph, name='complete_graph')
]
