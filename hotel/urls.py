from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hotel-list', views.hotel_list, name='hotel_list'),
    path('add/', views.hotel_add, name='hotel_add'),
    path('hotel/<int:pk>/edit/', views.hotel_edit, name='hotel_edit'),
    path('hotel/<int:pk>/delete/', views.hotel_delete, name='hotel_delete'),
    path('hotel/<int:hotel_id>/room/add/', views.room_add, name='room_add'),
    path('hotel/<int:hotel_id>/room/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('<int:hotel_id>/rooms/', views.room_list, name='room_list'),
    path('<int:hotel_id>/room/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('hotel/<int:hotel_id>/room/<int:room_id>/reservation/add/', views.reservation_add, name='reservation_add'),
    path('hotel/<int:hotel_id>/room/<int:room_id>/reservations/', views.reservation_list, name='reservation_list'),
    path('hotel/<int:hotel_id>/room/<int:room_id>/reservation/<int:reservation_id>/edit/', views.reservation_edit, name='reservation_edit'),
    path('hotel/<int:hotel_id>/room/<int:room_id>/reservation/<int:reservation_id>/status/<str:new_status>/', views.reservation_change_status, name='reservation_change_status'),
]