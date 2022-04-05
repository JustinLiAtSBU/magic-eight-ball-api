from django.urls import include, re_path
from magiceightball import views


urlpatterns = [
    re_path(r'^api/health', views.health),
    re_path(r'^api/motionpictures$', views.motion_picture_list),
    re_path(r'^api/motionpicture/$', views.motion_picture_detail),
    re_path(r'^api/movies$', views.movie_list),
    re_path(r'^api/movies/random$', views.random_movie),
    re_path(r'^api/tvshows$', views.tv_show_list),
    re_path(r'^api/tvshows/random$', views.random_tv_show),
]