from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    nume = models.CharField(max_length=128)
    imagine = models.CharField(max_length=128)
    tip = models.ForeignKey('EventType', on_delete=models.SET_NULL, null=True)
    locatie = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    ora_inceput = models.DateTimeField()
    ora_sfarsit = models.DateTimeField()
    descriere = models.CharField(max_length=256)

    def __str__(self):
        return self.nume

    def artisti(self):
        return list(map(lambda x: x.artist, EventArtist.objects.filter(event=self)))


class EventType(models.Model):
    nume = models.CharField(max_length=32)

    def __str__(self):
        return self.nume


class Location(models.Model):
    nume = models.CharField(max_length=128)
    oras = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.nume}, {self.oras}'

    def evenimente(self):
        return list(Event.objects.filter(locatie=self))

class City(models.Model):
    nume = models.CharField(max_length=128)

    def __str__(self):
        return self.nume

    def evenimente(self):
        return [event for locatie in Location.objects.filter(oras=self) for event in
                Event.objects.filter(locatie=locatie)]


class Artist(models.Model):
    nume = models.CharField(max_length=32)

    def __str__(self):
        return self.nume

    def evenimente(self):
        return list(map(lambda x: x.event, EventArtist.objects.filter(artist=self)))


class EventArtist(models.Model):
    event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True)
    artist = models.ForeignKey('Artist', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.event} - {self.artist}'


class TicketType(models.Model):
    event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True)
    nume = models.CharField(max_length=32)
    pret = models.IntegerField()
    nr_locuri = models.IntegerField()
    descriere = models.CharField(max_length=256)

    def __str__(self):
        return self.nume


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tip_bilet = models.ForeignKey('TicketType', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user} - {self.tip_bilet}'