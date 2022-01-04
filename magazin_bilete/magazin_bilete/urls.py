"""magazin_bilete URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('resetpass/', reset_password, name='reset_password'),
    path('', homepage, name='homepage'),
    path('tip/<int:type_id>', filter_by_event_type, name='filter_by_event_type'),
    path('oras/<int:city_id>', filter_by_city, name='filter_by_city'),
    path('cauta/<str:search_input>', filter_by_artist_event_location, name='filter_by_artist_event_location'),
    path('event/<int:event_id>', event_page, name='event_page'),
    path('cumpara/<int:ticket_id>', ticket_page, name='ticket_page'),
    path('ok', payment_accepted, name='payment_accepted'),
    path('account', account, name='account'),
]
