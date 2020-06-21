

from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

from .models import Location, Device, Link



###############################################################################
#####           ###############################################################
##### MAIN MENU ###############################################################
#####           ###############################################################
###############################################################################



def main_menu(request):
    return TemplateResponse(request, "main_menu.html")



###############################################################################
#####           ###############################################################
##### LOCATIONS ###############################################################
#####           ###############################################################
###############################################################################



def locations(request):
    if request.method == "POST":
        site_code = request.POST.get('site_code')
        site_name = request.POST.get('site_name')
        zip_code = request.POST.get('zip_code')
        city = request.POST.get('city')
        street = request.POST.get('street')
        site_code_sort = request.POST.get('site_code_sort')
        site_name_sort = request.POST.get('site_name_sort')
        zip_code_sort = request.POST.get('zip_code_sort')
        city_sort = request.POST.get('city_sort')
        street_sort = request.POST.get('street_sort')
    else:
        site_code = ''
        site_name = ''
        zip_code = ''
        city = ''
        street = ''
        site_code_sort = None
        site_name_sort = None
        zip_code_sort = None
        city_sort = None
        street_sort = None

    ##### SORT SECTION ########################################################

    if site_code_sort == '^':
        request.session['locations_sort'] = 'site_code'
    elif site_code_sort == 'v':
        request.session['locations_sort'] = '-site_code'
    elif site_code_sort == '=':
        request.session['locations_sort'] = None

    if site_name_sort == '^':
        request.session['locations_sort'] = 'site_name'
    elif site_name_sort == 'v':
        request.session['locations_sort'] = '-site_name'
    elif site_name_sort == '=':
        request.session['locations_sort'] = None

    if zip_code_sort == '^':
        request.session['locations_sort'] = 'zip_code'
    elif zip_code_sort == 'v':
        request.session['locations_sort'] = '-zip_code'
    elif zip_code_sort == '=':
        request.session['locations_sort'] = None

    if city_sort == '^':
        request.session['locations_sort'] = 'city'
    elif city_sort == 'v':
        request.session['locations_sort'] = '-city'
    elif city_sort == '=':
        request.session['locations_sort'] = None

    if street_sort == '^':
        request.session['locations_sort'] = 'street'
    elif street_sort == 'v':
        request.session['locations_sort'] = '-street'
    elif street_sort == '=':
        request.session['locations_sort'] = None

    ##### FILTER & ORDER SECTION ##############################################

    locations = Location.objects.filter(
        site_code__icontains=site_code,
        site_name__icontains=site_name,
        zip_code__icontains=zip_code,
        city__icontains=city,
        street__icontains=street
    )

    order = request.session.get('locations_sort')
    if order:
        locations = locations.order_by(order)

    ##### RENDER SECTION ######################################################

    values = []
    for location in locations:
        value = []
        value.append(location.id)
        value.append(location.site_code)
        value.append(location.site_name)
        value.append(location.zip_code)
        value.append(location.city)
        value.append(location.street)
        values.append(value)
    
    context = {
        'menu_page': 'locations',
        'title': 'Locations',
        'width': '100',
        'headers': ('','Site Code','Site Name','ZIP Code','City','Street'),
        'aligns': ('center','center','center','center','left','left'),
        'sorts': ('','site_code_sort','site_name_sort','zip_code_sort','city_sort','street_sort'),
        'filters': ({},
                    {'type': 'text', 'variable': 'site_code', 'label': 'filter', 'value': site_code},
                    {'type': 'text', 'variable': 'site_name', 'label': 'filter', 'value': site_name},
                    {'type': 'text', 'variable': 'zip_code', 'label': 'filter', 'value': zip_code},
                    {'type': 'text', 'variable': 'city', 'label': 'filter', 'value': city},
                    {'type': 'text', 'variable': 'street', 'label': 'filter', 'value': street}),
        'icons': ({'icon':'info','link':'/location'},
                  {'icon':'edit','link':'/edit-location'},
                  {'icon':'delete','link':'/delete-location'}),
        'values': values,
        'buttons': ({'name':'ADD LOCATION','link':'/add-location'},)
    }
    return TemplateResponse(request, "table.html", context)



###############################################################################
##### LOCATION DETAILS ########################################################
###############################################################################



def location(request,id):
    location = Location.objects.get(id=id)

    ##### DEVICE LIST SECTION #################################################

    devices = []
    devs = location.devices.all().order_by('name')
    for dev in devs:
        devices.append(dev.name)
    devices = '\n'.join(devices)

    ##### RENDER SECTION ######################################################

    values = {}
    values['ID:'] = location.id
    values['Site Code:'] = location.site_code
    values['Site Name:'] = location.site_name
    values['ZIP Code:'] = location.zip_code
    values['City:'] = location.city
    values['Street:'] = location.street
    values['Devices:'] = devices

    context = {
        'menu_page': 'locations',
        'title': 'Location Details',
        'width': '40',
        'header': location.site_code,
        'values': values,
        'message': '',
        'buttons': ({'name':'EDIT','link':'/edit-location/'+str(id)},
                    {'name':'BACK','link':'/locations'})
    }
    return TemplateResponse(request, "table_info.html", context)



###############################################################################
##### EDIT LOCATION ###########################################################
###############################################################################



def edit_location(request,id):
    message = ''
    location = Location.objects.get(id=id)

    if request.method == "POST":
        location.site_code = request.POST.get('site_code')
        location.site_name = request.POST.get('site_name')
        location.zip_code = request.POST.get('zip_code')
        location.city = request.POST.get('city')
        location.street = request.POST.get('street')
        try:
            location.save()
        except Exception as e:
            message = e
            location = Location.objects.get(id=id)

    ##### RENDER SECTION ######################################################

    values = {}
    values['Site Code:'] = {'variable': 'site_code', 'data': location.site_code}
    values['Site Name:'] = {'variable': 'site_name', 'data': location.site_name}
    values['ZIP Code:'] = {'variable': 'zip_code', 'data': location.zip_code}
    values['City:'] = {'variable': 'city', 'data': location.city}
    values['Street:'] = {'variable': 'street', 'data': location.street}

    context = {
        'menu_page': 'locations',
        'title': 'Edit Location',
        'width': '40',
        'header': location.site_code,
        'values': values,
        'message': message,
        'buttons': ({'name':'DETAILS','link':'/location/'+str(id)},
                    {'name':'DELETE','link':'/delete-location/'+str(id)},
                    {'name':'BACK','link':'/locations'},)
    }
    return TemplateResponse(request, "table_edit.html", context)



###############################################################################
##### ADD LOCATION ############################################################
###############################################################################



def add_location(request):
    message = ''

    if request.method == "POST":
        location = Location()
        location.site_code = request.POST.get('site_code')
        location.site_name = request.POST.get('site_name')
        location.zip_code = request.POST.get('zip_code')
        location.city = request.POST.get('city')
        location.street = request.POST.get('street')
        try:
            location.save()
            return redirect('/locations')
        except Exception as e:
            message = e

    ##### RENDER SECTION ######################################################

    values = {}
    values['Site Code:'] = {'variable': 'site_code'}
    values['Site Name:'] = {'variable': 'site_name'}
    values['ZIP Code:'] = {'variable': 'zip_code'}
    values['City:'] = {'variable': 'city'}
    values['Street:'] = {'variable': 'street'}

    context = {
        'menu_page': 'locations',
        'title': 'Add Location',
        'width': '40',
        'header': 'New Location',
        'values': values,
        'message': message,
        'buttons': ({'name':'BACK','link':'/locations'},)
    }
    return TemplateResponse(request, "table_edit.html", context)



###############################################################################
##### DELETE LOCATION #########################################################
###############################################################################



def delete_location(request,id):
    location = Location.objects.get(id=id)
    try:
        location.delete()
    except Exception as e:
        context = {
            'menu_page': 'locations',
            'title': 'Delete Location',
            'width': '40',
            'header': 'Error!',
            'message': e,
            'buttons': ({'name':'BACK','link':'/locations'},)
        }
        return TemplateResponse(request, "table_info.html", context)
    return redirect('/locations')



###############################################################################
#####         #################################################################
##### DEVICES #################################################################
#####         #################################################################
###############################################################################



def devices(request):
    if request.method == "POST":
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        is_root = True if request.POST.get('is_root') == 'on' else False
        location = request.POST.get('location')
        name_sort = request.POST.get('name_sort')
        desc_sort = request.POST.get('desc_sort')
        location_sort = request.POST.get('location_sort')
    else:
        name = ''
        desc = ''
        location = ''
        name_sort = None
        desc_sort = None
        location_sort = None

    ##### SORT SECTION ########################################################

    if name_sort == '^':
        request.session['devices_sort'] = 'name'
    elif name_sort == 'v':
        request.session['devices_sort'] = '-name'
    elif name_sort == '=':
        request.session['devices_sort'] = None

    if desc_sort == '^':
        request.session['devices_sort'] = 'desc'
    elif desc_sort == 'v':
        request.session['devices_sort'] = '-desc'
    elif desc_sort == '=':
        request.session['devices_sort'] = None

    if location_sort == '^':
        request.session['devices_sort'] = 'location__site_code'
    elif location_sort == 'v':
        request.session['devices_sort'] = '-location__site_code'
    elif location_sort == '=':
        request.session['devices_sort'] = None

    ##### FILTER & ORDER SECTION ##############################################

    devices = Device.objects.filter(
        name__icontains=name,
        desc__icontains=desc,
        location__site_code__icontains=location,
    )

    order = request.session.get('devices_sort')
    if order:
        devices = devices.order_by(order)

    ##### RENDER SECTION ######################################################

    values = []
    for device in devices:
        value = []
        value.append(device.id)
        value.append(device.name)
        value.append(device.desc)
        value.append('Yes' if device.is_root else 'No')
        value.append(device.location.site_code)
        values.append(value)

    context = {
        'menu_page': 'devices',
        'title': 'Devices',
        'width': '80',
        'headers': ('','Name','Description','Root','Location'),
        'aligns': ('center','left','center','center','center'),
        'sorts': ('','name_sort','desc_sort','','location_sort'),
        'filters': ({},
                    {'type': 'text', 'variable': 'name', 'label': 'filter', 'value': name},
                    {'type': 'text', 'variable': 'desc', 'label': 'filter', 'value': desc},
                    {},
                    {'type': 'text', 'variable': 'location', 'label': 'filter', 'value': location}),
        'icons': ({'icon':'info','link':'/device'},
                  {'icon':'edit','link':'/edit-device'},
                  {'icon':'delete','link':'/delete-device'}),
        'values': values,
        'buttons': ({'name':'ADD DEVICE','link':'/add-device'},)
    }
    return TemplateResponse(request, "table.html", context)



###############################################################################
##### DEVICE DETAILS ##########################################################
###############################################################################



def device(request,id):
    device = Device.objects.get(id=id)

    ##### RENDER SECTION ######################################################

    values = {}
    values['ID:'] = device.id
    values['Name:'] = device.name
    values['Description:'] = device.desc
    values['Root:'] = 'Yes' if device.is_root else 'No'
    values['Location:'] = device.location

    context = {
        'menu_page': 'devices',
        'title': 'Device Details',
        'width': '40',
        'header': device.name,
        'values': values,
        'message': '',
        'buttons': ({'name':'EDIT','link':'/edit-device/'+str(id)},
                    {'name':'BACK','link':'/devices'})
    }
    return TemplateResponse(request, "table_info.html", context)



###############################################################################
##### EDIT DEVICE #############################################################
###############################################################################



def edit_device(request,id):
    message = ''
    device = Device.objects.get(id=id)

    if request.method == "POST":
        device.name = request.POST.get('name')
        device.desc = request.POST.get('desc')
        device.is_root = True if request.POST.get('is_root') == 'on' else False
        device.location = Location.objects.get(id=request.POST.get('location_id'))
        try:
            device.save()
        except Exception as e:
            message = e
            device = Device.objects.get(id=id)

    ##### OPTIONS SECTION #####################################################

    locations = []
    locs = Location.objects.all().order_by('site_code')
    for loc in locs:
        location = {}
        location['id'] = loc.id
        location['desc'] = loc.site_code + ' / ' + loc.site_name + ' / ' + loc.city
        locations.append(location)

    ##### RENDER SECTION ######################################################

    values = {}
    values['Name:'] = {'variable': 'name', 'data': device.name}
    values['Description:'] = {'variable': 'desc', 'data': device.desc}
    values['Root:'] = {'variable': 'is_root', 'checkbox': device.is_root}
    values['Location:'] = {'variable': 'location_id', 'data': device.location.id, 'options': locations}

    context = {
        'menu_page': 'devices',
        'title': 'Edit Device',
        'width': '40',
        'header': device.name,
        'values': values,
        'message': message,
        'buttons': ({'name':'DETAILS','link':'/device/'+str(id)},
                    {'name':'DELETE','link':'/delete-device/'+str(id)},
                    {'name':'BACK','link':'/devices'},)
    }
    return TemplateResponse(request, "table_edit.html", context)



###############################################################################
##### ADD DEVICE ##############################################################
###############################################################################



def add_device(request):
    message = ''

    if request.method == "POST":
        device = Device()
        device.name = request.POST.get('name')
        device.desc = request.POST.get('desc')
        device.is_root = True if request.POST.get('is_root') == 'on' else False
        device.location = Location.objects.get(id=request.POST.get('location_id'))
        try:
            device.save()
            return redirect('/devices')
        except Exception as e:
            message = e

    ##### OPTIONS SECTION #####################################################

    locations = []
    locs = Location.objects.all().order_by('site_code')
    for loc in locs:
        location = {}
        location['id'] = loc.id
        location['desc'] = loc.site_code + ' / ' + loc.site_name + ' / ' + loc.city
        locations.append(location)

    ##### RENDER SECTION ######################################################

    values = {}
    values['Name:'] = {'variable': 'name'}
    values['Description:'] = {'variable': 'desc'}
    values['Root:'] = {'variable': 'is_root', 'checkbox': False}
    values['Location:'] = {'variable': 'location_id', 'options': locations}

    context = {
        'menu_page': 'devices',
        'title': 'Add Device',
        'width': '40',
        'header': 'New Device',
        'values': values,
        'message': message,
        'buttons': ({'name':'BACK','link':'/devices'},)
    }
    return TemplateResponse(request, "table_edit.html", context)



###############################################################################
##### DELETE DEVICE ###########################################################
###############################################################################



def delete_device(request,id):
    device = Device.objects.get(id=id)
    try:
        device.delete()
    except Exception as e:
        context = {
            'menu_page': 'devices',
            'title': 'Delete Device',
            'width': '40',
            'header': 'Error!',
            'message': e,
            'buttons': ({'name':'BACK','link':'/devices'},)
        }
        return TemplateResponse(request, "table_info.html", context)
    return redirect('/devices')



###############################################################################
#####       ###################################################################
##### LINKS ###################################################################
#####       ###################################################################
###############################################################################



def links(request):
    if request.method == "POST":
        site_code = request.POST.get('site_code')
        from_name = request.POST.get('from_name')
        to_name = request.POST.get('to_name')
        site_code_sort = request.POST.get('site_code_sort')
        from_name_sort = request.POST.get('from_name_sort')
        to_name_sort = request.POST.get('to_name_sort')
    else:
        site_code = ''
        from_name = ''
        to_name = ''
        site_code_sort = None
        from_name_sort = None
        to_name_sort = None

    ##### SORT SECTION ########################################################

    if site_code_sort == '^':
        request.session['links_sort'] = 'device__location__site_code'
    elif site_code_sort == 'v':
        request.session['links_sort'] = '-device__location__site_code'
    elif site_code_sort == '=':
        request.session['links_sort'] = None

    if from_name_sort == '^':
        request.session['links_sort'] = 'from_device__name'
    elif from_name_sort == 'v':
        request.session['links_sort'] = '-from_device__name'
    elif from_name_sort == '=':
        request.session['links_sort'] = None

    if to_name_sort == '^':
        request.session['links_sort'] = 'to_device__name'
    elif to_name_sort == 'v':
        request.session['links_sort'] = '-to_device__name'
    elif to_name_sort == '=':
        request.session['links_sort'] = None

    ##### FILTER & ORDER SECTION ##############################################

    links = Link.objects.filter(
        from_device__location__site_code__icontains=site_code,
        from_device__name__icontains=from_name,
        to_device__name__icontains=to_name,
    )

    order = request.session.get('links_sort')
    if order:
        links = links.order_by(order)

    ##### RENDER SECTION ######################################################

    values = []
    for link in links:
        value = []
        value.append(link.id)
        value.append(link.from_device.location.site_code)
        value.append(link.from_device.name)
        value.append('⟹')
        value.append(link.to_device.name)
        values.append(value)

    context = {
        'menu_page': 'links',
        'title': 'Links',
        'width': '70',
        'headers': ('','Location','Device','','Device'),
        'aligns': ('center','center','center','center','center'),
        'sorts': ('','from_site_code_sort','from_name_sort','','to_name_sort'),
        'filters': ({},
                    {'type': 'text', 'variable': 'site_code', 'label': 'filter', 'value': site_code},
                    {'type': 'text', 'variable': 'from_name', 'label': 'filter', 'value': from_name},
                    {},
                    {'type': 'text', 'variable': 'to_name', 'label': 'filter', 'value': to_name}),
        'icons': ({'icon':'info','link':'/link'},
                  {'icon':'edit','link':'/edit-link'},
                  {'icon':'delete','link':'/delete-link'}),
        'values': values,
        'buttons': ({'name':'ADD LINK','link':'/add-link'},)
    }
    return TemplateResponse(request, "table.html", context)



###############################################################################
##### LINK DETAILS ############################################################
###############################################################################



def link(request,id):
    link = Link.objects.get(id=id)

    ##### RENDER SECTION ######################################################

    values = {}
    values['Source Device:'] = link.from_device.name
    values[''] = '⇓'
    values['Destination Device'] = link.to_device.name

    context = {
        'menu_page': 'links',
        'title': 'Link Details',
        'width': '40',
        'header': 'Link no. {}'.format(link.id),
        'values': values,
        'message': '',
        'buttons': ({'name':'EDIT','link':'/edit-link/'+str(id)},
                    {'name':'BACK','link':'/links'})
    }
    return TemplateResponse(request, "table_info.html", context)



###############################################################################
##### EDIT LINK ###############################################################
###############################################################################



def edit_link(request,id):
    message = ''
    link = Link.objects.get(id=id)

    if request.method == "POST":
        link.to_device = Device.objects.get(id=request.POST.get('to_device'))
        try:
            link.save()
            link.from_device.save()
        except Exception as e:
            message = e
            link = Link.objects.get(id=id)

    ##### OPTIONS SECTION #####################################################

    location = link.from_device.location

    devices = []
    devs = location.devices.all().exclude(id=link.from_device.id).order_by('name')
    for dev in devs:
        device = {}
        device['id'] = dev.id
        device['desc'] = dev.name
        devices.append(device)

    ##### RENDER SECTION ######################################################

    values = {}
    values['Link To:'] = {'variable': 'to_device', 'data': link.to_device.id, 'options': devices}

    context = {
        'menu_page': 'links',
        'title': 'Edit Link',
        'width': '40',
        'header': link.from_device.name,
        'values': values,
        'message': message,
        'buttons': ({'name':'DETAILS','link':'/link/'+str(id)},
                    {'name':'DELETE','link':'/delete-link/'+str(id)},
                    {'name':'BACK','link':'/links'},)
    }
    return TemplateResponse(request, "table_edit.html", context)



###############################################################################
##### ADD LINK ################################################################
###############################################################################



def add_link(request):
    message = ''
    location = ''

    if request.method == "POST":
        link = Link()
        link.from_device = Device.objects.get(id=request.POST.get('from_device_id'))
        to_device_id = request.POST.get('to_device_id')
        if to_device_id:
            link.to_device = Device.objects.get(id=to_device_id)
            try:
                if link.from_device == link.to_device:
                    raise Exception('Connections to self are not allowed!')
                link.save()
                link.from_device.save()
                return redirect('/links')
            except Exception as e:
                message = e
        else:
            location = link.from_device.location

    ##### OPTIONS SECTION #####################################################

    devices = []
    if location == '':
        devs = Device.objects.all().order_by('name')
    else:
        devs = location.devices.all().order_by('name')
    for dev in devs:
        device = {}
        device['id'] = dev.id
        device['desc'] = dev.name
        devices.append(device)

    ##### RENDER SECTION ######################################################

    values = {}
    if location == '':
        values['Source Device:'] = {'variable': 'from_device_id', 'options': devices}
        values['Destination Device:'] = {'variable': 'to_device_id', 'options': [{'desc':'click SAVE to unlock'},]}
    else:
        values['Source Device:'] = {'variable': 'from_device_id', 'data': link.from_device.id, 'options': devices}
        values['Destination Device:'] = {'variable': 'to_device_id', 'options': devices}

    context = {
        'menu_page': 'links',
        'title': 'Add Link',
        'width': '40',
        'header': 'New Link',
        'values': values,
        'message': message,
        'buttons': ({'name':'BACK','link':'/links'},)
    }
    return TemplateResponse(request, "table_edit.html", context)



###############################################################################
##### DELETE LINK #############################################################
###############################################################################



def delete_link(request,id):
    link = Link.objects.get(id=id)
    try:
        link.delete()
        link.from_device.save()
    except Exception as e:
        context = {
            'menu_page': 'links',
            'title': 'Delete Link',
            'width': '40',
            'header': 'Error!',
            'message': e,
            'buttons': ({'name':'BACK','link':'/links'},)
        }
        return TemplateResponse(request, "table_info.html", context)
    return redirect('/links')



###############################################################################
#####            ##############################################################
##### SIMULATION ##############################################################
#####            ##############################################################
###############################################################################



def simulation(request):
    message = ''

    if request.method == "POST":
        location_id = request.POST.get('location_id')
        try:
            devices = Device.objects.filter(location__id=location_id)
            for device in devices:
                device.failure = False
                device.save()
            links = Link.objects.filter(from_device__location__id=location_id)
            for link in links:
                link.failure = False
                link.save()
            return redirect('/simulation/{}'.format(location_id))
        except Exception as e:
            message = e

    ##### OPTIONS SECTION #####################################################

    locations = []
    locs = Location.objects.all().order_by('site_code')
    for loc in locs:
        location = {}
        location['id'] = loc.id
        location['desc'] = loc.site_code + ' / ' + loc.site_name + ' / ' + loc.city
        locations.append(location)

    ##### RENDER SECTION ######################################################

    values = {}
    values['Location:'] = {'variable': 'location_id', 'options': locations}

    context = {
        'menu_page': 'simulation',
        'title': 'Simulation',
        'width': '40',
        'header': 'Select Location',
        'values': values,
        'message': message,
    }
    return TemplateResponse(request, "table_edit.html", context)



###############################################################################
#####              ############################################################
##### LOCATION SIM ############################################################
#####              ############################################################
###############################################################################



def sim_check(device):
    if (not device.sim_check) and (not device.failure):
        device.sim_check = True
        device.save()
        updevices = device.uplinks.all()
        for updevice in updevices:###############################################################################
            links = Link.objects.filter(from_device=device,to_device=updevice)
            for link in links:
                if not link.failure:
                    sim_check(updevice)
        downdevices = device.downlinks.all()
        for downdevice in downdevices:
            links = Link.objects.filter(from_device=downdevice,to_device=device)
            for link in links:
                if not link.failure:
                    sim_check(downdevice)



def simulate(location):
    devices = location.devices.all()
    for device in devices:
        device.sim_check = False
        device.save()
    root_devices = location.devices.filter(is_root=True)
    for root_device in root_devices:
        sim_check(root_device)



def location_sim(request,location_id):
    if request.method == "POST":
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        is_root = True if request.POST.get('is_root') == 'on' else False
        from_name = request.POST.get('from_name')
        to_name = request.POST.get('to_name')
        name_sort = request.POST.get('name_sort')
        desc_sort = request.POST.get('desc_sort')
        from_name_sort = request.POST.get('from_name_sort')
        to_name_sort = request.POST.get('to_name_sort')
    else:
        name = ''
        desc = ''
        from_name = ''
        to_name = ''
        name_sort = None
        desc_sort = None
        from_name_sort = None
        to_name_sort = None

    ##### SORT SECTION ########################################################

    if name_sort == '^':
        request.session['loc_sim_dev_sort'] = 'name'
    elif name_sort == 'v':
        request.session['loc_sim_dev_sort'] = '-name'
    elif name_sort == '=':
        request.session['loc_sim_dev_sort'] = None

    if desc_sort == '^':
        request.session['loc_sim_dev_sort'] = 'desc'
    elif desc_sort == 'v':
        request.session['loc_sim_dev_sort'] = '-desc'
    elif desc_sort == '=':
        request.session['loc_sim_dev_sort'] = None

    if from_name_sort == '^':
        request.session['loc_sim_link_sort'] = 'from_device__name'
    elif from_name_sort == 'v':
        request.session['loc_sim_link_sort'] = '-from_device__name'
    elif from_name_sort == '=':
        request.session['loc_sim_link_sort'] = None

    if to_name_sort == '^':
        request.session['loc_sim_link_sort'] = 'to_device__name'
    elif to_name_sort == 'v':
        request.session['loc_sim_link_sort'] = '-to_device__name'
    elif to_name_sort == '=':
        request.session['loc_sim_link_sort'] = None

    ##### FILTER & ORDER SECTION ##############################################

    location = Location.objects.get(id=location_id)

    devices = location.devices.filter(name__icontains=name,desc__icontains=desc)

    order = request.session.get('loc_sim_dev_sort')
    if order:
        devices = devices.order_by(order)

    links = Link.objects.filter(
        from_device__name__icontains=from_name,
        to_device__name__icontains=to_name,
        from_device__location__id=location_id
    )

    order = request.session.get('loc_sim_link_sort')
    if order:
        links = links.order_by(order)

    ##### RENDER SECTION ######################################################

    if request.method == "GET":
        simulate(location)

    dev_values = []
    for device in devices:
        dev_value = []
        dev_value.append(device.id)
        dev_value.append(device.name)
        dev_value.append(device.desc)
        dev_value.append('Yes' if device.is_root else 'No')
        if device.failure:
            dev_value.append('FAILURE')
        elif device.sim_check:
            dev_value.append('OK')
        else:
            dev_value.append('NO UPLINK')
        dev_values.append(dev_value)

    link_values = []
    for link in links:
        link_value = []
        link_value.append(link.id)
        link_value.append(link.from_device.name)
        link_value.append('⟹')
        link_value.append(link.to_device.name)
        link_value.append('FAILURE') if link.failure else link_value.append('OK')
        link_values.append(link_value)

    context = {
        'menu_page': 'simulation',
        'title': 'Failure Simulation for ' + device.location.site_code + ' Location',
        'width': '60',
        'dev_headers': ('','Name','Description','Root','Device Status'),
        'dev_aligns': ('center','left','center','center','center'),
        'dev_sorts': ('','name_sort','desc_sort','',''),
        'dev_filters': ({},
                        {'type': 'text', 'variable': 'name', 'label': 'filter', 'value': name},
                        {'type': 'text', 'variable': 'desc', 'label': 'filter', 'value': desc},
                        {},
                        {}),
        'dev_values': dev_values,
        'link_headers': ('','Device','','Device','Link Status'),
        'link_aligns': ('center','center','center','center','center'),
        'link_sorts': ('','from_name_sort','','to_name_sort',''),
        'link_filters': ({},
                    {'type': 'text', 'variable': 'from_name', 'label': 'filter', 'value': from_name},
                    {},
                    {'type': 'text', 'variable': 'to_name', 'label': 'filter', 'value': to_name},
                    {}),
        'link_values': link_values,
        'buttons': ({'name':'BACK','link':'/simulation'},)
    }
    return TemplateResponse(request, "simulation.html", context)



###############################################################################
##### DEVICE TOGGLE ###########################################################
###############################################################################



def device_toggle(request,id):
    device = Device.objects.get(id=id)
    location_id = device.location.id
    device.failure ^= True
    try:
        device.save()
    except Exception as e:
        context = {
            'menu_page': 'simulation',
            'title': 'Device Toggle',
            'width': '20',
            'header': 'Error!',
            'message': e,
            'buttons': ({'name':'BACK','link':'/simulation/{}'.format(location_id)},)
        }
        return TemplateResponse(request, "table_info.html", context)
    return redirect('/simulation/{}'.format(location_id))



###############################################################################
##### LINK TOGGLE #############################################################
###############################################################################



def link_toggle(request,id):
    link = Link.objects.get(id=id)
    location_id = link.from_device.location.id
    link.failure ^= True
    try:
        link.save()
    except Exception as e:
        context = {
            'menu_page': 'simulation',
            'title': 'Link Toggle',
            'width': '20',
            'header': 'Error!',
            'message': e,
            'buttons': ({'name':'BACK','link':'/simulation/{}'.format(location_id)},)
        }
        return TemplateResponse(request, "table_info.html", context)
    return redirect('/simulation/{}'.format(location_id))
