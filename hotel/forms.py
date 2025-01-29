import datetime
from django import forms
from .models import Hotel, Reservation, Room, Event, Service

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'image']
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [ 'name', 'description', 'start_date', 'end_date', 'image']
        widgets = {
        'start_date': forms.DateInput(attrs={'type': 'date'}),
        'end_date': forms.DateInput(attrs={'type': 'date'}),
    }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [ 'name', 'description', 'price', ]
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [ 'name', 'description', 'price', 'image']
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer_name', 'customer_email', 'customer_phone', 'check_in', 'check_out', 'services']

    widgets = {
        'check_in': forms.DateInput(attrs={'type': 'date'}),
        'check_out': forms.DateInput(attrs={'type': 'date'}),
    }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view
        room = kwargs.pop('room', None)  # Get the room from the view
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user = user  # Assign the user to the reservation instance if available
        if room:
            self.room = room  # Save the room instance for validation later

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            today = datetime.date.today()

            # Validate dates
            if check_in < today:
                self.add_error('check_in', 'Check-in date cannot be in the past.')
            if check_out < today:
                self.add_error('check_out', 'Check-out date cannot be in the past.')
            if check_in >= check_out:
                self.add_error('check_out', 'Check-out date must be after check-in date.')
            if check_in == check_out:
                self.add_error('check_out', 'Check-out date cannot be the same as check-in date.')

            # Check for overlapping reservations for the same room
            if hasattr(self, 'room'):  # Ensure that we have a room instance
                overlapping_reservations = Reservation.objects.filter(
                    room=self.room,
                    check_in__lt=check_out,  # If check-in date is before the new check-out date
                    check_out__gt=check_in   # If check-out date is after the new check-in date
                )

                # If there are any overlapping reservations, raise a validation error
                if overlapping_reservations.exists():
                    raise forms.ValidationError('The selected room is already booked')

        return cleaned_data
