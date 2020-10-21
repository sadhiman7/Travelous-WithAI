from django.contrib import admin

# Register your models here.
from .models import Tours, PlaceToVisit, HowToReach, Bookings, blogs, comments

admin.site.register(Tours)
admin.site.register(PlaceToVisit)
admin.site.register(HowToReach)
admin.site.register(Bookings)
admin.site.register(blogs)
admin.site.register(comments)