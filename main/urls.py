from django.urls import path
from .views import base, show_category, about, MapPointsAPI, profile_view,mark_notifications_as_read

urlpatterns = [
    path('', base, name='base'),
    path('category/<str:slug>/', show_category, name='category_detail'),
    path('about/', about, name='about'),
    path('api/points/', MapPointsAPI.as_view(), name='map_points_api'),
    path('profile/', profile_view, name='profile'),
    path('mark_notifications_as_read/', mark_notifications_as_read, name='mark_notifications_as_read'),

]
