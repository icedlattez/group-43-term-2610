from django.shortcuts import render, get_object_or_404
from .models import Owner, Stall


# OWNER LIST
def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner/owner_list.html', {'owners': owners})


# OWNER DETAIL
def owner_detail(request, id):
    owner = get_object_or_404(Owner, id=id)
    return render(request, 'owner/owner_detail.html', {'owner': owner})


# EDIT OWNER
def owner_edit(request, id):
    owner = get_object_or_404(Owner, id=id)

    if request.method == "POST":
        owner.name = request.POST['name']
        owner.phone = request.POST['phone']
        owner.social_media = request.POST['social_media']
        owner.description = request.POST['description']
        owner.save()

    return render(request, 'owner/owner_edit.html', {'owner': owner})


# STALL LIST
def stall_list(request):
    stalls = Stall.objects.select_related('owner').all()
    return render(request, 'owner/stall_list.html', {'stalls': stalls})


# STALL DETAIL
def stall_detail(request, id):
    stall = get_object_or_404(Stall, id=id)
    return render(request, 'owner/stall_detail.html', {'stall': stall})


# CREATE STALL
def stall_create(request):
    if request.method == "POST":
        Stall.objects.create(
            owner_id=1,  # TEMP (you can fix later with login user)
            name=request.POST['name'],
            description=request.POST['description'],
            location=request.POST['location'],
            capacity=request.POST['capacity'],
            rental_fee=request.POST['rental_fee']
        )

    return render(request, 'owner/stall_create.html')


# EDIT STALL
def stall_edit(request, id):
    stall = get_object_or_404(Stall, id=id)

    if request.method == "POST":
        stall.name = request.POST['name']
        stall.description = request.POST['description']
        stall.location = request.POST['location']
        stall.capacity = request.POST['capacity']
        stall.rental_fee = request.POST['rental_fee']
        stall.save()

    return render(request, 'owner/stall_edit.html', {'stall': stall})