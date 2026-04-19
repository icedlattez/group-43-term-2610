from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Event, EventRegistration
from .forms import EventForm


# ------------------------
# EVENT LIST
# ------------------------
@login_required
def event_list(request):
    now = timezone.now()
    events = Event.objects.all()

    ongoing = []
    future = []
    past = []

    for event in events:
        if event.start_date <= now <= event.end_date:
            ongoing.append(event)
        elif event.start_date > now:
            future.append(event)
        else:
            past.append(event)

    return render(request, 'events/event_list.html', {
        'ongoing': ongoing,
        'future': future,
        'past': past,
    })


# ------------------------
# EVENT DETAIL
# ------------------------
@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, id=pk)

    is_registered = EventRegistration.objects.filter(
        user=request.user,
        event=event
    ).exists()

    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered
    })


# ------------------------
# DASHBOARD
# ------------------------
@login_required
def dashboard(request):
    registrations = EventRegistration.objects.filter(user=request.user)

    return render(request, 'events/dashboard.html', {
        'registrations': registrations
    })


# ------------------------
# CREATE EVENT
# ------------------------
@login_required
def create_event(request):
    form = EventForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.save()
        return redirect('home')

    return render(request, 'events/create_event.html', {
        'form': form
    })