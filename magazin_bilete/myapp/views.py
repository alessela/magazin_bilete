from django.shortcuts import render
from .models import *

user = None
is_login = True
is_signup = True
ticket_type = None
type = None


def login(request):
    global user
    global is_login
    global is_signup
    is_login = True
    is_signup = False
    user = None
    return render(request, 'login.html')


def signup(request):
    global is_login
    global is_signup
    is_login = False
    is_signup = True
    return render(request, 'signup.html')


def reset_password(request):
    global is_login
    global is_signup
    is_login = is_signup = False
    return render(request, 'reset_password.html')


def homepage(request):
    global user
    global is_login
    global is_signup
    if request.method != 'POST':
        return render(request, 'homepage.html',
                      {'user': user, 'events': Event.objects.all(), 'cities': City.objects.all(),
                       'event_types': EventType.objects.all(), 'locations': Location.objects.all(),
                       'no_events': 'Nu sunt evenimente disponibile' if not Event.objects.all() else ''})
    if is_login:
        if User.objects.filter(username=request.POST['username']):
            user = User.objects.get(username=request.POST['username'])
            return render(request, 'homepage.html',
                          {'user': user, 'events': Event.objects.all(), 'cities': City.objects.all(),
                           'event_types': EventType.objects.all(), 'locations': Location.objects.all(),
                           'no_events': 'Nu sunt evenimente disponibile' if not Event.objects.all() else ''})
        if User.objects.filter(email=request.POST['username']):
            user = User.objects.get(email=request.POST['username'])
            return render(request, 'homepage.html',
                          {'user': user, 'events': Event.objects.all(), 'cities': City.objects.all(),
                           'event_types': EventType.objects.all(), 'locations': Location.objects.all(),
                           'no_events': 'Nu sunt evenimente disponibile' if not Event.objects.all() else ''})
        return render(request, 'login.html', {'msg': 'Parola, nume de utilizator sau email gresit!'})

    if is_signup:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'msg': 'Nume de utilizator deja folosit!'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'msg': 'Acest email este deja asociat unui cont!'})
        User.objects.create_user(username=username, email=email, password=password,
                                 first_name=request.POST['first_name'],
                                 last_name=request.POST['last_name'])
        user = User.objects.get(username=username)
        return render(request, 'homepage.html',
                      {'user': user, 'events': Event.objects.all(), 'cities': City.objects.all(),
                       'event_types': EventType.objects.all(), 'locations': Location.objects.all(),
                       'no_events': 'Nu sunt evenimente disponibile' if not Event.objects.all() else ''})

    username = request.POST['username']
    new_password = request.POST['password']
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=request.POST['username'])
        user.password = new_password
        user.save()
        return render(request, 'homepage.html',
                      {'user': user, 'events': Event.objects.all(), 'cities': City.objects.all(),
                       'event_types': EventType.objects.all(), 'locations': Location.objects.all(),
                       'no_events': 'Nu sunt evenimente disponibile' if not Event.objects.all() else ''})
    if User.objects.filter(email=username).exists():
        user = User.objects.get(email=request.POST['username'])
        user.password = new_password
        user.save()
        return render(request, 'homepage.html',
                      {'user': user, 'events': Event.objects.all(), 'cities': City.objects.all(),
                       'event_types': EventType.objects.all(), 'locations': Location.objects.all(),
                       'no_events': 'Nu sunt evenimente disponibile' if not Event.objects.all() else ''})
    return render(request, 'reset_password.html', {'msg': 'Cont inexistent'})


def filter_by_event_type(request, type_id):
    global user
    tip = EventType.objects.get(pk=type_id)
    evenimente = Event.objects.filter(tip=tip)
    return render(request, 'homepage.html',
                  {'user': user, 'events': evenimente, 'cities': City.objects.all(),
                   'event_types': EventType.objects.all(), 'locations': Location.objects.all(),
                   'title': f'Evenimente {tip}',
                   'no_events': 'Nu sunt evenimente disponibile' if not evenimente else ''})


def filter_by_city(request, city_id):
    global user
    oras = City.objects.get(pk=city_id)
    return render(request, 'homepage.html',
                  {'user': user, 'events': oras.evenimente(), 'cities': City.objects.all(),
                   'event_types': EventType.objects.all(), 'locations': Location.objects.all(),
                   'title': f'Evenimente in {oras}',
                   'no_events': 'Nu sunt evenimente disponibile' if not oras.evenimente() else ''})


def filter_by_artist_event_location(request, search_input):
    global user
    evenimente = list(set((Artist.objects.get(nume=search_input).evenimente() if Artist.objects.filter(
        nume=search_input) else []) + \
                          list(filter((lambda ev: search_input in ev.nume), Event.objects.all())) + \
                          (Location.objects.get(nume=search_input).evenimente() if Location.objects.filter(
                              nume=search_input) else [])))
    return render(request, 'homepage.html',
                  {'user': user, 'events': evenimente, 'cities': City.objects.all(),
                   'event_types': EventType.objects.all(), 'locations': Location.objects.all(),
                   'title': f'Rezultatele cautarii dupa {search_input}',
                   'no_events': 'Nu sunt evenimente disponibile' if not evenimente else ''})


def event_page(request, event_id):
    global user
    event = Event.objects.get(pk=event_id)
    return render(request, 'event_page.html', {'user': user, 'event': event, 'artists': event.artisti(),
                                               'tickets': TicketType.objects.filter(event=event)})


def ticket_page(request, ticket_id):
    global ticket_type
    global user
    ticket_type = TicketType.objects.get(pk=ticket_id)
    return render(request, 'ticket_page.html', {'user': user, 'ticket': ticket_type})


def payment_accepted(request):
    global user
    global ticket_type
    Ticket.objects.create(user=user, tip_bilet=ticket_type)
    return render(request, 'success.html', {'user': user})


def account(request):
    global user
    if request.method != 'POST':
        return render(request, 'account.html',
                      {'user': user, 'tickets': Ticket.objects.filter(user=user)})

    new_username = request.POST['username']
    new_email = request.POST['email']

    if User.objects.filter(username=new_username).exists() and user.username != new_username:
        return render(request, 'account.html', {'user': user, 'tickets': Ticket.objects.filter(user=user),
                                                'err': 'Nume de utilizator deja folosit!'})
    if User.objects.filter(email=new_email).exists() and user.email != new_email:
        return render(request, 'account.html', {'user': user, 'tickets': Ticket.objects.filter(user=user),
                                                'err': 'Acest email este deja asociat unui cont!'})
    user.username = new_username
    user.password = request.POST['password']
    user.email = new_email
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.save()
    return render(request, 'account.html',
                  {'user': user, 'tickets': Ticket.objects.filter(user=user), 'msg': 'Date schimbate cu succes'})