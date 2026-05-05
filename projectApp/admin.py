from django.contrib import admin
from .models import Student, StudyRoom, Booking


# Register your models here.
admin.site.register(Student)
admin.site.register(StudyRoom)
admin.site.register(Booking)