from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<choose>/<int:num>/<searchwords>/<tagged>', views.find, name='search'),
    path('question/<int:num>', views.question, name='question'),
    path('post', views.post, name='post'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('setting', views.setting, name='setting'),
]
