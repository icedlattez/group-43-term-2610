from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Vendor, Stall
from .forms import StallForm


# ========================= VENDOR =========================

def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor/vendor_list.html', {'vendors': vendors})


def vendor_detail(request, id):
    vendor = get_object_or_404(Vendor, id=id)
    return render(request, 'vendor/vendor_detail.html', {'vendor': vendor})


def vendor_edit(request, id):
    vendor = get_object_or_404(Vendor, id=id)

    if request.method == "POST":
        vendor.name = request.POST.get('name')
        vendor.phone = request.POST.get('phone')
        vendor.social_media = request.POST.get('social_media')
        vendor.description = request.POST.get('description')
        vendor.save()
        return redirect('vendor_list')

    return render(request, 'vendor/vendor_edit.html', {'vendor': vendor})


# ========================= STALL =========================

def stall_list(request):
    stalls = Stall.objects.select_related('vendor').all()
    return render(request, 'vendor/stall_list.html', {'stalls': stalls})


def stall_create(request):
    if request.method == "POST":
        form = StallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stall_list')
    else:
        form = StallForm()

    return render(request, 'vendor/stall_create.html', {'form': form})


def stall_edit(request, id):
    stall = get_object_or_404(Stall, id=id)

    if request.method == "POST":
        form = StallForm(request.POST, instance=stall)
        if form.is_valid():
            form.save()
            return redirect('stall_list')
    else:
        form = StallForm(instance=stall)

    return render(request, 'vendor/stall_edit.html', {'form': form})


# ========================= HOME =========================

@login_required
def home(request):
    vendors = Vendor.objects.all()
    stalls = Stall.objects.select_related('vendor').all()

    return render(request, 'vendor/home.html', {
        'vendors': vendors,
        'stalls': stalls,
    })

from django.shortcuts import render, get_object_or_404
from .models import Stall

# STALL LIST
def stall_list(request):
    stalls = Stall.objects.select_related('vendor').all()
    return render(request, 'vendor/stall_list.html', {'stalls': stalls})


# DASHBOARD
def stall_dashboard(request):
    stalls = Stall.objects.all()

    total_stalls = stalls.count()
    total_capacity = sum(s.capacity for s in stalls)
    total_fee = sum(float(s.rental_fee) for s in stalls)

    return render(request, 'vendor/stall_dashboard.html', {
        'stalls': stalls,
        'total_stalls': total_stalls,
        'total_capacity': total_capacity,
        'total_fee': total_fee,
    })