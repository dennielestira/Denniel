from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, Reservation, Room
from .forms import HotelForm, ReservationForm, RoomForm
from django.shortcuts import redirect

# Hotel Views
def index(request):
    a_hotel = Hotel.objects.count()
    return render(request, 'hotel/index.html')

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel/hotel_list.html', {'hotels': hotels})

def hotel_add(request):
    if request.method == 'POST':

        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm()
    return render(request, 'hotel/hotel_form.html', {'form': form})

def hotel_edit(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm(instance=hotel)  # Use the form with existing hotel data
    return render(request, 'hotel/edit_hotel.html', {'form': form, 'hotel': hotel})


def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    hotel.delete()
    return redirect('hotel_list')

def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    rooms = hotel.rooms.all()

    # Get all reservations for each room
    for room in rooms:
        room.bookings = Reservation.objects.filter(room=room)

    return render(request, 'hotel/room_list.html', {'hotel': hotel, 'rooms': rooms})


def room_add(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)  # Fetch hotel by ID
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)  # Bind the POST data and files to the form
        if form.is_valid():
            room = form.save(commit=False)  # Don't save the room yet
            room.hotel = hotel  # Associate the room with the hotel
            room.save()  # Now save the room
            return redirect('room_list', hotel_id=hotel.id)  # Redirect to room list view for that hotel
    else:
        form = RoomForm()  # Initialize the form if GET request
    
    return render(request, 'hotel/room_form.html', {'form': form, 'hotel': hotel})



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


def room_delete(request, hotel_id, pk):
    room = get_object_or_404(Room, pk=pk)
    room.delete()
    return redirect('room_list', hotel_id=hotel_id)
# Reservation Views
def reservation_add(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(Room, pk=room_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.room = room  # Link the selected room
            reservation.save()
            return redirect('reservation_list', hotel_id=hotel.id, room_id=room.id)
    else:
        form = ReservationForm()
    
    return render(request, 'hotel/reservation_form.html', {'form': form, 'hotel': hotel, 'room': room})

def reservation_list(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)  # Get the hotel by ID
    room = get_object_or_404(Room, pk=room_id)    # Get the room by ID
    reservations = Reservation.objects.filter(room=room)  # Get the reservations for that room

    return render(request, 'hotel/reservation_list.html', {
        'hotel': hotel,  # Ensure 'hotel' is passed to the template
        'room': room,    # Ensure 'room' is passed to the template
        'reservations': reservations
    })


    return render(request, 'hotel/reservation_list.html', {'room': room, 'reservations': reservations})
def reservation_edit(request, hotel_id, room_id, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_list', hotel_id=hotel_id, room_id=room_id)
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'hotel/reservation_form.html', {'form': form, 'hotel_id': hotel_id, 'room_id': room_id, 'reservation': reservation})
def reservation_change_status(request, hotel_id, room_id, reservation_id, new_status):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if new_status in dict(Reservation.STATUS_CHOICES):
        reservation.status = new_status
        reservation.save()
    return redirect('reservation_list', hotel_id=hotel_id, room_id=room_id)