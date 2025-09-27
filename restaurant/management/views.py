from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def post_login_redirect(request):
    """
    Redirectusers based on their role.
    """
    user = request.user
    # If statement to redirect user
    if user.is_superuser:
        # redirect to dashboard
        return redirect('management:home')
    else: 
        # regular customers -> to landing page
        return redirect('home:index')


@login_required
def management_home(request):
    """
    Render the dashboard only for superusers
    """
    if not request.user.is_superuser:
        return redirect('home:index')
    return render(request, 'dashboard.html')