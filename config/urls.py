"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include

from eems.urls import router as eems_router

import eems.views as eems_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', eems_views.IndexView.as_view()),
    path('log/', eems_views.LogView.as_view(), name='log'),
    path('reservation_calendar/', eems_views.Reservation_CalendarView.as_view(), name='reservation_calendar'),
    path('reservation_table/', eems_views.Reservation_TableView.as_view(), name='reservation_table'),
    path('qrcode', eems_views.qrcode, name='qrcode'),  # for qrcode_line_bot
    path('webhook', eems_views.webhook, name='webhook'),
    path('api/', include(eems_router.urls)),  # for api
]
