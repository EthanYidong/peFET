"""peFET URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from .views import account, event, functions, portal

urlpatterns = [
    path('event/', include([
        path('all', event.all),
        path('create', event.create),
        path('<int:event_id>/', include([
            path('update', event.update),
            path('send_emails', functions.send_emails),
            path('participants/', include([
                path('', event.read_participants),
                path('create', event.create_participant),
                path('create_csv', event.create_participants_csv),
                path('<int:participant_id>/', include([
                    path('update', event.update_participant),
                    path('get_submission', event.get_participant_submission),
                ])),
            ])),
        ]))
    ])),
    path('account/', include([
        path('signup', account.signup),
        path('login', account.login),
        path('complete_tutorial', account.complete_tutorial),
        path('me', account.me),
    ])),
    path('portal/', include([
        path('qr_code', portal.qr_code),
        path('upload_image', portal.upload_image),
    ]))
]
