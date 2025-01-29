
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, Reservation, Room, Service, Event
from .forms import EventForm, HotelForm, ReservationForm, RoomForm, ServiceForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Admin permission check for editing/deleting content
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# User registration view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'hotel/register.html', {'form': form})

# User login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('hotel_list')  # Redirect to appointment list after login
    else:
        form = AuthenticationForm()
    return render(request, 'hotel/login.html', {'form': form})

# User logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'hotel/index.html')

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel/hotel_list.html', {'hotels': hotels})

@login_required
@admin_required
def hotel_add(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm()
    return render(request, 'hotel/hotel_form.html', {'form': form})

@login_required
@admin_required
def hotel_edit(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'hotel/edit_hotel.html', {'form': form, 'hotel': hotel})

@login_required
@admin_required
def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    hotel.delete()
    return redirect('hotel_list')


def event_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    events = hotel.events.all()
    return render(request, 'hotel/event_list.html', {'hotel': hotel, 'events': events})

@login_required
@admin_required
def event_add(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.hotel = hotel
            event.save()
            return redirect('event_list', hotel_id=hotel.id)
    else:
        form = EventForm()
    
    return render(request, 'hotel/event_form.html', {'form': form, 'hotel': hotel})

@login_required
@admin_required
def event_edit(request, hotel_id, pk):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list', hotel_id=hotel.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'hotel/event_edit.html', {'form': form, 'hotel': hotel, 'event': event})

@login_required
@admin_required
def event_delete(request, hotel_id, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('event_list', hotel_id=hotel_id)

def service_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    services = hotel.services.all()
    return render(request, 'hotel/service_list.html', {'hotel': hotel, 'services': services})

@login_required
@admin_required
def service_add(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.hotel = hotel
            service.save()
            return redirect('service_list', hotel_id=hotel.id)
    else:
        form = ServiceForm()
    
    return render(request, 'hotel/service_form.html', {'form': form, 'hotel': hotel})

@login_required
@admin_required
def service_edit(request, hotel_id, pk):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    service = get_object_or_404(Service, pk=pk)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list', hotel_id=hotel.id)
    else:
        form = ServiceForm(instance=service)

    return render(request, 'hotel/service_edit.html', {'form': form, 'hotel': hotel, 'service': service})

@login_required
@admin_required
def service_delete(request, hotel_id, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('service_list', hotel_id=hotel_id)

def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    rooms = hotel.rooms.all()

    for room in rooms:
        room.bookings = Reservation.objects.filter(room=room)

    return render(request, 'hotel/room_list.html', {'hotel': hotel, 'rooms': rooms})

@login_required
@admin_required
def room_add(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            return redirect('room_list', hotel_id=hotel.id)
    else:
        form = RoomForm()
    
    return render(request, 'hotel/room_form.html', {'form': form, 'hotel': hotel})

@login_required
@admin_required
def room_edit(request, hotel_id, pk):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list', hotel_id=hotel.id)
    else:
        form = RoomForm(instance=room)

    return render(request, 'hotel/room_edit.html', {'form': form, 'hotel': hotel, 'room': room})

@login_required
@admin_required
def room_delete(request, hotel_id, pk):
    room = get_object_or_404(Room, pk=pk)
    room.delete()
    return redirect('room_list', hotel_id=hotel_id)

@login_required
def reservation_add(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(Room, pk=room_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user, room=room)  # Pass room to the form
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.room = room  # Assign the room to the reservation
            reservation.hotel = hotel  # Assign the hotel to the reservation
            reservation.save()
            return redirect('user_reservation_list')
    else:
        form = ReservationForm(user=request.user, room=room)  # Pass room to the form
    
    return render(request, 'hotel/reservation_form.html', {'form': form, 'hotel': hotel, 'room': room})








def reservation_edit(request, hotel_id, room_id, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('user_reservation_list')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'hotel/reservation_form.html', {'form': form, 'hotel_id': hotel_id, 'room_id': room_id, 'reservation': reservation})

@login_required
def reservation_change_status(request, hotel_id, room_id, reservation_id, new_status):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if new_status in dict(Reservation.STATUS_CHOICES):
        reservation.status = new_status
        reservation.save()
    return redirect('user_reservation_list')
@login_required
def user_reservation_list(request):
    # Get user's reservations if not an admin
    if not request.user.is_staff:
        reservations = Reservation.objects.filter(user=request.user)
    else:
        reservations = None  # Admin shouldn't see their own bookings here

    # Get all reservations for admin users
    all_bookings = Reservation.objects.all() if request.user.is_staff else None

    return render(request, 'hotel/user_reservation_list.html', {
        'reservations': reservations,
        'all_bookings': all_bookings,
    })