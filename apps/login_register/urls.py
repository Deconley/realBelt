
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,),
    url(r'^register$', views.register, name = "register"),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success, name = 'success'),
    url(r'^profile/(?P<id>\d+)$', views.profile, name = 'profile'),
    url(r'^add-friend/(?P<id>\d+)$', views.addFriend, name='add-friend'),
    url(r'^remove-friend/(?P<id>\d+)$', views.removeFriend, name='remove-friend'),

]
