import datetime
from django import forms
from .models import Hotel, Reservation, Room

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'image']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [ 'name', 'description', 'price', 'image']
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        room = forms.ModelChoiceField(queryset=Room.objects.filter(available=True), empty_label="Select a room", required=True)
        fields = ['customer_name', 'customer_email', 'customer_phone', 'check_in', 'check_out', 'room']

    # Using HTML5 date picker widget
    widgets = {
        'check_in': forms.DateInput(attrs={'type': 'date'}),
        'check_out': forms.DateInput(attrs={'type': 'date'}),
    }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        # Ensure the check-in and check-out dates are valid
        if check_in and check_out:
            today = datetime.date.today()

            # Check if check-in or check-out is in the past
            if check_in < today:
                self.add_error('check_in', 'Check-in date cannot be in the past.')
            if check_out < today:
                self.add_error('check_out', 'Check-out date cannot be in the past.')

            # Ensure check-out is after check-in
            if check_in >= check_out:
                self.add_error('check_out', 'Check-out date must be after check-in date.')

            # Ensure check-in and check-out are not the same day
            if check_in == check_out:
                self.add_error('check_out', 'Check-out date cannot be the same as check-in date.')

            # Check for overlapping reservations for the room
            overlapping_reservations = Reservation.objects.filter(
                room=cleaned_data.get('room'),
                check_in__lt=check_out,  # Check if the reservation starts before the selected check-out
                check_out__gt=check_in   # Check if the reservation ends after the selected check-in
            )

            if overlapping_reservations.exists():
                raise forms.ValidationError('The room is already booked for the selected dates. Please choose another date.')

        return cleaned_data
