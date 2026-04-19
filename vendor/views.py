from django.shortcuts import render, get_object_or_404, redirect
from .models import Vendor, Stall


# ---------------- VENDOR ----------------

def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor/vendor_list.html', {'vendors': vendors})


def vendor_detail(request, id):
    vendor = get_object_or_404(Vendor, id=id)
    return render(request, 'vendor/vendor_detail.html', {'vendor': vendor})


def vendor_edit(request, id):
    vendor = get_object_or_404(Vendor, id=id)
    return render(request, 'vendor/vendor_edit.html', {'vendor': vendor})


# ---------------- STALL ----------------

def stall_list(request):
    stalls = Stall.objects.all()
    return render(request, 'vendor/stall_list.html', {'stalls': stalls})


def stall_create(request):
    vendors = Vendor.objects.all()

    if request.method == "POST":
        vendor_id = request.POST.get('vendor')
        stall_name = request.POST.get('stall_name')
        location = request.POST.get('location')
        event_name = request.POST.get('event_name')

        vendor = get_object_or_404(Vendor, id=vendor_id)

        Stall.objects.create(
            vendor=vendor,
            stall_name=stall_name,
            location=location,
            event_name=event_name
        )

        return redirect('stall_list')  # IMPORTANT FIX

    return render(request, 'vendor/stall_create.html', {'vendors': vendors})