from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfessionalSignupForm
from .models import CustomUser 

def signup_view(request):
    if request.method == 'POST':
        form = ProfessionalSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = ProfessionalSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'accounts/logout_confirm.html')

@login_required
def profile_view(request):
    context = {'user': request.user}
    if request.user.role == 'admin':
        pending_requests = CustomUser.objects.filter(role='student', is_organizer_requested=True)
        context['pending_requests'] = pending_requests
    return render(request, 'accounts/profile.html', context)

@login_required
def request_organizer_view(request):
    if request.method == 'POST':
        user = request.user
    
        if user.role == 'student' and not user.is_rejected:
            user.is_organizer_requested = True
            user.save()
            messages.success(request, "Request sent to Admin.")
        else:
            messages.error(request, "You are not eligible to request this role.")
        return redirect('profile')
    return redirect('profile')

@login_required
def approve_organizer_view(request, user_id):
    if request.user.role != 'admin':
        messages.error(request, "Access Denied.")
        return redirect('home')
    
    if request.method == 'POST':
        target_user = get_object_or_404(CustomUser, id=user_id)
        target_user.role = 'organizer'
        target_user.is_organizer_requested = False
        target_user.is_rejected = False 
        target_user.save()
        messages.success(request, f"{target_user.username} is now an Organizer!")
    
    return redirect('profile')

@login_required
def reject_organizer_view(request, user_id):
    if request.user.role != 'admin':
        messages.error(request, "Access Denied.")
        return redirect('home')
    
    if request.method == 'POST':
        target_user = get_object_or_404(CustomUser, id=user_id)
        target_user.is_organizer_requested = False
        target_user.is_rejected = True
        target_user.save()
        messages.warning(request, f"Request for {target_user.username} has been rejected.")
    
    return redirect('profile')