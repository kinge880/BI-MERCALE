from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
   path('' , views.powerbi, name = 'index'),
   path('requestbi/', views.requestBi, name = 'requestbi'),
]
