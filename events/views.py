from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from .models import Event, EventRegistration
from .forms import (
    EventForm,
    ConcertRegistrationForm,
    TournamentRegistrationForm,
    BazaarRegistrationForm
)

# =========================================================
# EVENT LIST
# =========================================================
@login_required
def event_list(request):
    now = timezone.now()
    events = Event.objects.all()

    ongoing, future, past = [], [], []

    for event in events:

        if not event.start_date or not event.end_date:
            ongoing.append(event)
            continue

        if event.end_date < now:
            past.append(event)

        elif event.start_date > now:
            future.append(event)

        else:
            ongoing.append(event)

    return render(request, 'events/event_list.html', {
        'ongoing': ongoing,
        'future': future,
        'past': past,
    })


# =========================================================
# EVENT DETAIL
# =========================================================
@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, id=pk)

    if event.status != 'approved' and request.user != event.organizer and request.user.role != 'admin':
        return redirect('home')

    is_registered = EventRegistration.objects.filter(
        user=request.user,
        event=event
    ).exists()

    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'now': timezone.now(),
    })


# =========================================================
# REGISTER EVENT
# =========================================================
@login_required
def register_event(request, pk):
    event = get_object_or_404(Event, id=pk)
    now = timezone.now()

    if event.status != 'approved':
        return redirect('event_detail', pk=pk)

    if event.end_date and event.end_date < now:
        return redirect('event_detail', pk=pk)

    form_map = {
        'concert': ConcertRegistrationForm,
        'tournament': TournamentRegistrationForm,
        'bazaar': BazaarRegistrationForm,
    }

    form_class = form_map.get(event.event_type, ConcertRegistrationForm)

    existing = EventRegistration.objects.filter(
        user=request.user,
        event=event
    ).first()

    form = form_class(request.POST or None)

    if request.method == "POST" and form.is_valid():

        if existing:
            return redirect('event_detail', pk=pk)

        EventRegistration.objects.create(
            user=request.user,
            event=event,
            data=form.cleaned_data
        )

        return redirect('event_detail', pk=pk)

    return render(request, 'events/register.html', {
        'form': form,
        'event': event,
    })


# =========================================================
# EDIT EVENT
# =========================================================
@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, id=pk)

    # Only organizer or admin can edit
    if event.organizer != request.user and request.user.role != 'admin':
        return redirect('event_detail', pk=pk)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)

        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {
        'form': form,
        'event': event
    })


# =========================================================
# DASHBOARD
# =========================================================
@login_required
def dashboard(request):
    registrations = EventRegistration.objects.select_related('event').filter(
        user=request.user
    )

    concert_regs = []
    tournament_regs = []
    bazaar_regs = []

    for reg in registrations:

        if reg.event.event_type == 'concert':
            concert_regs.append(reg)

        elif reg.event.event_type == 'tournament':
            tournament_regs.append(reg)

        elif reg.event.event_type == 'bazaar':
            bazaar_regs.append(reg)

    return render(request, 'events/dashboard.html', {
        'concert_regs': concert_regs,
        'tournament_regs': tournament_regs,
        'bazaar_regs': bazaar_regs,
    })


# =========================================================
# CREATE EVENT
# =========================================================
@login_required
def create_event(request):
    # Security check for role
    if request.user.role not in ['organizer', 'admin']:
        messages.error(request, "Access denied.")
        return redirect('home')

    form = EventForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.status = 'pending'
        event.save()
        return redirect('home')

    return render(request, 'events/create_event.html', {
        'form': form
    })