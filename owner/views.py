from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from events.models import Event
from .models import Owner, Stall


def can_manage_stall(user):
    return user.is_authenticated and getattr(user, "role", None) != "student"


def is_event_organizer(user, stall):
    return (
        user.is_authenticated and
        stall.event is not None and
        stall.event.organizer == user
    )


def is_stall_owner(user, stall):
    return (
        user.is_authenticated and
        stall.owner is not None and
        stall.owner.user_id == user.id
    )


def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner/owner_list.html', {'owners': owners})


def owner_detail(request, id):
    owner = get_object_or_404(Owner, id=id)
    return render(request, 'owner/owner_detail.html', {'owner': owner})


@login_required
def owner_edit(request, id):
    if not can_manage_stall(request.user):
        return redirect('owner_detail', id=id)

    owner = get_object_or_404(Owner, id=id)

    if request.method == "POST":
        owner.name = request.POST.get('name')
        owner.phone = request.POST.get('phone')
        owner.social_media = request.POST.get('social_media')
        owner.description = request.POST.get('description')
        owner.save()
        return redirect('owner_detail', id=owner.id)

    return render(request, 'owner/owner_edit.html', {'owner': owner})


def stall_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')

    stalls = Stall.objects.select_related('owner', 'event').exclude(status='rejected')

    if query:
        stalls = stalls.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(owner__name__icontains=query) |
            Q(event__title__icontains=query)
        )

    if status == "active":
        stalls = stalls.filter(is_active=True)
    elif status == "inactive":
        stalls = stalls.filter(is_active=False, status='pending')

    event_stalls = stalls.filter(event__isnull=False)
    rental_stalls = stalls.filter(event__isnull=True)

    return render(request, 'owner/stall_list.html', {
        'stalls': stalls,
        'event_stalls': event_stalls,
        'rental_stalls': rental_stalls,
        'query': query,
        'status': status
    })


def stall_detail(request, id):
    stall = get_object_or_404(Stall, id=id)
    return render(request, 'owner/stall_detail.html', {'stall': stall})


@login_required
def rejected_stall_list(request):
    if getattr(request.user, "role", None) == "student":
        return redirect('stall_list')

    stalls = Stall.objects.select_related('owner', 'event').filter(status='rejected')

    return render(request, 'owner/rejected_stall_list.html', {
        'stalls': stalls
    })


@login_required
def stall_create(request):
    if not can_manage_stall(request.user):
        return redirect('stall_list')

    owner = Owner.objects.filter(user=request.user).first()
    events = Event.objects.all()

    if request.method == "POST":
        event_id = request.POST.get('event_id')

        event = None
        if event_id:
            event = get_object_or_404(Event, id=event_id)

        Stall.objects.create(
            owner=owner,
            event=event,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            location=request.POST.get('location'),
            capacity=int(request.POST.get('capacity') or 1),
            rental_fee=float(request.POST.get('rental_fee') or 0),
            stall_image=request.FILES.get('stall_image'),
            rental_start_date=request.POST.get('rental_start_date') or None,
            rental_end_date=request.POST.get('rental_end_date') or None,
            is_active=False,
            status='pending',
        )

        return redirect('stall_list')

    return render(request, 'owner/stall_create.html', {
        'owner': owner,
        'events': events
    })


@login_required
def stall_approve(request, id):
    stall = get_object_or_404(Stall, id=id)

    if not is_event_organizer(request.user, stall):
        return redirect('stall_list')

    stall.is_active = True
    stall.status = 'approved'
    stall.save()

    return redirect('stall_list')


@login_required
def stall_reject(request, id):
    stall = get_object_or_404(Stall, id=id)

    if not is_event_organizer(request.user, stall):
        return redirect('stall_list')

    stall.is_active = False
    stall.status = 'rejected'
    stall.save()

    return redirect('stall_list')


@login_required
def stall_edit(request, id):
    stall = get_object_or_404(Stall, id=id)

    if not (
        is_event_organizer(request.user, stall) or
        is_stall_owner(request.user, stall)
    ):
        return redirect('stall_detail', id=id)

    events = Event.objects.all()

    if request.method == "POST":
        event_id = request.POST.get('event_id')

        if event_id:
            stall.event = get_object_or_404(Event, id=event_id)
        else:
            stall.event = None

        stall.name = request.POST.get('name')
        stall.description = request.POST.get('description')
        stall.location = request.POST.get('location')
        stall.capacity = int(request.POST.get('capacity') or 1)
        stall.rental_fee = float(request.POST.get('rental_fee') or 0)
        stall.rental_start_date = request.POST.get('rental_start_date') or None
        stall.rental_end_date = request.POST.get('rental_end_date') or None

        if request.FILES.get('stall_image'):
            stall.stall_image = request.FILES.get('stall_image')

        stall.save()

        return redirect('stall_detail', id=stall.id)

    return render(request, 'owner/stall_edit.html', {
        'stall': stall,
        'events': events
    })


@login_required
def stall_delete(request, id):
    stall = get_object_or_404(Stall, id=id)

    if not (
        is_event_organizer(request.user, stall) or
        is_stall_owner(request.user, stall)
    ):
        return redirect('stall_detail', id=id)

    if request.method == "POST":
        stall.delete()
        return redirect('stall_list')

    return render(request, 'owner/stall_delete.html', {
        'stall': stall
    })


def stall_by_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    stalls = Stall.objects.select_related('owner', 'event').filter(
        event=event,
        is_active=True
    ).exclude(status='rejected')

    return render(request, 'owner/stall_by_event.html', {
        'event': event,
        'stalls': stalls
    })