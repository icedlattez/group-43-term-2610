from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Vendor, Stall
from .forms import VendorForm, StallForm
from events.models import Event


# =========================================================
# VENDOR
# =========================================================

@login_required
def vendor_list(request):
    # only vendors that belong to events
    vendors = Vendor.objects.select_related('event').all()

    return render(request, 'vendor/vendor_list.html', {
        'vendors': vendors
    })


@login_required
def vendor_detail(request, id):
    vendor = get_object_or_404(Vendor.objects.select_related('event'), id=id)
    stalls = vendor.stalls.all()

    return render(request, 'vendor/vendor_detail.html', {
        'vendor': vendor,
        'stalls': stalls
    })


# 🔥 CREATE VENDOR UNDER EVENT (IMPORTANT RULE)
@login_required
def create_vendor(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    form = VendorForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        vendor = form.save(commit=False)
        vendor.user = request.user
        vendor.event = event
        vendor.save()

        return redirect('event_detail', pk=event.id)

    return render(request, 'vendor/vendor_create.html', {
        'form': form,
        'event': event
    })


@login_required
def vendor_edit(request, id):
    vendor = get_object_or_404(Vendor, id=id)

    form = VendorForm(request.POST or None, instance=vendor)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('vendor_detail', id=vendor.id)

    return render(request, 'vendor/vendor_edit.html', {
        'form': form,
        'vendor': vendor
    })


# =========================================================
# STALL
# =========================================================

@login_required
def stall_list(request):
    stalls = Stall.objects.select_related('vendor', 'vendor__event').all()

    return render(request, 'vendor/stall_list.html', {
        'stalls': stalls
    })


# 🔥 CREATE STALL UNDER VENDOR (EVENT → VENDOR → STALL FLOW)
@login_required
def stall_create(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)

    form = StallForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        stall = form.save(commit=False)
        stall.vendor = vendor
        stall.save()

        return redirect('vendor_detail', id=vendor.id)

    return render(request, 'vendor/stall_create.html', {
        'form': form,
        'vendor': vendor
    })


@login_required
def stall_edit(request, id):
    stall = get_object_or_404(Stall, id=id)

    form = StallForm(request.POST or None, instance=stall)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('stall_list')

    return render(request, 'vendor/stall_edit.html', {
        'form': form,
        'stall': stall
    })


# =========================================================
# HOME (EVENT → VENDORS → STALLS)
# =========================================================

@login_required
def home(request):
    events = Event.objects.prefetch_related(
        'vendors',
        'vendors__stalls'
    ).all()

    return render(request, 'vendor/home.html', {
        'events': events
    })