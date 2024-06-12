"""VRO_RSO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import sysVRO.views
from VRO_RSO import settings
from sysVRO.views import index_page, events_page, profile_page, ProfileEditView, detachments_page, detachment_page, \
    joining_page, profile_events_page, DetachmentUpdateView, about_page, coming_soon_page, page_404, agreements_page, logout_view
from django.contrib.auth.views import LoginView, LogoutView
from sysVRO.views import SignUp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='index'),
    path('home/', index_page),
    # path('', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path("signup/", SignUp.as_view(), name='signup'),

    path("agreements/", agreements_page, name='agreements'),


    path("about/", about_page, name='about'),
    path("about/contacts/", coming_soon_page, name='coming_soon'),
    path("about/gallery/", coming_soon_page, name='coming_soon'),
    path("about/news/", coming_soon_page, name='coming_soon'),
    path("employment/", coming_soon_page, name='coming_soon'),

    path("events/", events_page, name='events'),
    path('events/create/', sysVRO.views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:event_id>/', sysVRO.views.event_page, name='event'),
    path('events/<int:pk>/edit', sysVRO.views.EventUpdateView.as_view(), name='event_edit'),
    path('events/<int:event_id>/take_part', sysVRO.views.take_part, name='event_take_part'),

    path("profile/", profile_page, name='profile'),
    path("profile/detachment/", DetachmentUpdateView.as_view(), name='profile_detachment'),
    path("profile/events/", profile_events_page, name='profile_events'),
    path("profile/settings/", ProfileEditView.as_view(), name='profile_settings'),

    path("joining/", joining_page, name='joining'),
    path("joining/detachments/", detachments_page, name='detachments'),
    path("joining/detachments/<int:detachment_id>/", detachment_page, name='detachment'),
    path("joining/detachments/<int:detachment_id>/edit", sysVRO.views.DetachmentUpdateView1.as_view(), name='detachment_edit'),

    path("404/", page_404, name='404'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

