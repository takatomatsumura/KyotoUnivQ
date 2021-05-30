from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<searchwords>/<tagged>', views.find, name='search'),
]
