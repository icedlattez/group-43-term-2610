from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProfessionalSignupForm
from .models import User  

# ---------------- AUTH VIEWS ----------------

def signup_view(request):
    if request.method == 'POST':
        form = ProfessionalSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('vendor_home')
    else:
        form = ProfessionalSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('vendor_home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')

# ---------------- STUDENT ACTION ----------------

@login_required
def request_lecturer_status(request):
    """Fired when Student clicks 'Be Organizer'"""
    request.user.is_approving = True
    request.user.save()
    return redirect('vendor_home')

# ---------------- ADMIN APPROVAL ----------------

@staff_member_required
def admin_approval_list(request):
    """View for Admin to see who clicked 'Be Organizer'"""
    pending_users = User.objects.filter(is_approving=True, role='student')
    # CRITICAL: This must match your filename exactly (admin_approval.html)
    return render(request, 'accounts/admin_approval.html', {'pending_users': pending_users})

@staff_member_required
def approve_user(request, user_id):
    """Action for Admin to officially upgrade a student"""
    user_to_approve = get_object_or_404(User, id=user_id)
    user_to_approve.role = 'organizer' 
    user_to_approve.is_approving = False 
    user_to_approve.save()
    return redirect('admin_approval_list')