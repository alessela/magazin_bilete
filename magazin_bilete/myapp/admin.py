from django.contrib import admin

from .models import *

admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Location)
admin.site.register(City)
admin.site.register(Artist)
admin.site.register(EventArtist)
admin.site.register(TicketType)
admin.site.register(Ticket)
