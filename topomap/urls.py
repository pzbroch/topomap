"""topomap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from topomapper.views import main_menu, locations, devices, links
from topomapper.views import location, edit_location, add_location, delete_location
from topomapper.views import device, edit_device, add_device, delete_device
from topomapper.views import link, edit_link, add_link, delete_link
from topomapper.views import simulation, location_sim, device_toggle, link_toggle


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_menu),

    path('locations/', locations),
    path('location/<int:id>', location),
    path('edit-location/<int:id>', edit_location),
    path('add-location/', add_location),
    path('delete-location/<int:id>', delete_location),

    path('devices/', devices),
    path('device/<int:id>', device),
    path('edit-device/<int:id>', edit_device),
    path('add-device/', add_device),
    path('delete-device/<int:id>', delete_device),

    path('links/', links),
    path('link/<int:id>', link),
    path('edit-link/<int:id>', edit_link),
    path('add-link/', add_link),
    path('delete-link/<int:id>', delete_link),

    path('simulation/', simulation),
    path('simulation/<int:location_id>', location_sim),
    path('simulation/dev-toggle/<int:id>', device_toggle),
    path('simulation/link-toggle/<int:id>', link_toggle),
]
