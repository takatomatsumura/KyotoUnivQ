from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<choose>/<searchwords>/<tagged>', views.find, name='search'),
    path('search/<choose>/<tagged>', views.findByTag, name='searchByTag'),
    path('question/<int:num>', views.question, name='question'),
    path('post', views.post, name='post'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('setting', views.setting, name='setting'),
    path('next_signup', views.next_signup, name='next_signup'),
    path('tag', views.tag, name='tag'),
]
