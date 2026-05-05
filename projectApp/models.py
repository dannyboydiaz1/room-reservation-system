from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class StudyRoom(models.Model):
    room_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.room_name


class Booking(models.Model):
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20)

    # student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE)

    def clean(self):
        # Prevent invalid time
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")

        # Prevent overlapping bookings
        overlapping = Booking.objects.filter(
            room=self.room,
            booking_date=self.booking_date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )

        if overlapping.exists():
            raise ValidationError("This room is already booked for this time.")

    def __str__(self):
        return f"{self.room} - {self.booking_date}"