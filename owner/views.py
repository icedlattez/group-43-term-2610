from django.shortcuts import render, get_object_or_404, redirect
from .models import Owner, Stall
from events.models import Event


# ================= OWNER =================
def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner/owner_list.html', {'owners': owners})


def owner_detail(request, id):
    owner = get_object_or_404(Owner, id=id)
    return render(request, 'owner/owner_detail.html', {'owner': owner})


def owner_edit(request, id):
    owner = get_object_or_404(Owner, id=id)

    if request.method == "POST":
        owner.name = request.POST.get('name')
        owner.phone = request.POST.get('phone')
        owner.social_media = request.POST.get('social_media')
        owner.description = request.POST.get('description')
        owner.save()

        return redirect('owner_detail', id=owner.id)

    return render(request, 'owner/owner_edit.html', {'owner': owner})


# ================= STALL =================
def stall_list(request):
    stalls = Stall.objects.select_related('owner', 'event').all()
    return render(request, 'owner/stall_list.html', {'stalls': stalls})


def stall_detail(request, id):
    stall = get_object_or_404(Stall, id=id)
    return render(request, 'owner/stall_detail.html', {'stall': stall})


# ================= CREATE STALL (FIXED) =================
def stall_create(request):
    owner = Owner.objects.first()
    events = Event.objects.all()

    if request.method == "POST":

        event_id = request.POST.get('event_id')

        # SAFE EVENT HANDLING
        event = None
        if event_id:
            try:
                event = Event.objects.get(id=int(event_id))
            except (ValueError, Event.DoesNotExist):
                event = None

        Stall.objects.create(
            owner=owner,
            event=event,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            location=request.POST.get('location'),
            capacity=int(request.POST.get('capacity') or 0),
            rental_fee=float(request.POST.get('rental_fee') or 0)
        )

        return redirect('stall_list')

    return render(request, 'owner/stall_create.html', {
        'owner': owner,
        'events': events
    })


# ================= EDIT STALL =================
def stall_edit(request, id):
    stall = get_object_or_404(Stall, id=id)

    if request.method == "POST":
        stall.name = request.POST.get('name')
        stall.description = request.POST.get('description')
        stall.location = request.POST.get('location')
        stall.capacity = int(request.POST.get('capacity') or 0)
        stall.rental_fee = float(request.POST.get('rental_fee') or 0)
        stall.save()

        return redirect('stall_detail', id=stall.id)

    return render(request, 'owner/stall_edit.html', {'stall': stall})

# ================= DELETE STALL =================
def stall_delete(request, id):
    stall = get_object_or_404(Stall, id=id)

    if request.method == "POST":
        stall.delete()
        return redirect('stall_list')

    return render(request, 'owner/stall_delete.html', {
        'stall': stall
    })

# ================= EVENT → STALLS =================
def stall_by_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    stalls = Stall.objects.select_related('owner').filter(event=event)

    return render(request, 'owner/stall_by_event.html', {
        'event': event,
        'stalls': stalls
    })