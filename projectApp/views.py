from django.shortcuts import render, redirect
from django.contrib import messages
# from flask import request
from .models import StudyRoom, Booking, Student
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Booking
from django.shortcuts import get_object_or_404




# Create your views here.

def home(request):
    rooms = StudyRoom.objects.all()
    return render(request, 'home.html', {'rooms': rooms})


@login_required
def book_room(request):
    if request.method == "POST":
        try:
            booking = Booking(
                student=request.user,
                room_id=request.POST['room'],
                booking_date=request.POST['date'],
                start_time=request.POST['start'],
                end_time=request.POST['end'],
                status='confirmed'
            )

            booking.full_clean()  # runs validation
            booking.save()

            messages.success(request, "Room booked successfully!")
            return redirect('my_bookings')

        except Exception as e:
            messages.error(request, str(e))

    rooms = StudyRoom.objects.all()
    return render(request, 'book.html', {'rooms': rooms})


def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def my_bookings(request):
    # print("THIS IS MY BOOKINGS VIEW")  # 👈 ADD THIS

    bookings = Booking.objects.filter(student=request.user).order_by('-booking_date')

    return render(request, 'my_bookings.html', {
        'bookings': bookings
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, student=request.user)
    booking.delete()
    messages.success(request, "Booking cancelled successfully!")
    return redirect('my_bookings')