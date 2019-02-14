from django.urls import path,re_path
from .views import (SearchProductView)

urlpatterns = [
    path('search/',SearchProductView.as_view(),name='query'),

    ]