from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hotel-list', views.hotel_list, name='hotel_list'),
    path('add/', views.hotel_add, name='hotel_add'),
    path('hotel/<int:pk>/edit/', views.hotel_edit, name='hotel_edit'),
    path('hotel/<int:pk>/delete/', views.hotel_delete, name='hotel_delete'),
    path('hotel/<int:hotel_id>/events/', views.event_list, name='event_list'),
    path('hotel/<int:hotel_id>/event/add/', views.event_add, name='event_add'),
    path('hotel/<int:hotel_id>/event/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('hotel/<int:hotel_id>/event/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('hotel/<int:hotel_id>/services/', views.service_list, name='service_list'),
    path('hotel/<int:hotel_id>/service/add/', views.service_add, name='service_add'),
    path('hotel/<int:hotel_id>/service/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('hotel/<int:hotel_id>/service/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('hotel/<int:hotel_id>/room/add/', views.room_add, name='room_add'),
    path('hotel/<int:hotel_id>/room/<int:pk>/delete/', views.room_delete, name='room_delete'),
    path('hotel/<int:hotel_id>/room/<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('<int:hotel_id>/rooms/', views.room_list, name='room_list'),
    path('hotel/<int:hotel_id>/room/<int:room_id>/reservation/add/', views.reservation_add, name='reservation_add'),
    path('hotel/<int:hotel_id>/room/<int:room_id>/reservation/<int:reservation_id>/edit/', views.reservation_edit, name='reservation_edit'),
    path('hotel/<int:hotel_id>/room/<int:room_id>/reservation/<int:reservation_id>/status/<str:new_status>/', views.reservation_change_status, name='reservation_change_status'),
    path('my-reservations/', views.user_reservation_list, name='user_reservation_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]