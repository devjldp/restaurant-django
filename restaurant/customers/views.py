from django.shortcuts import render, redirect
from django.contrib import messages


#import models
from .models import CustomerProfile

#import forms
from .forms import CustomerProfileForm


# Create your views here.
def create_profile(request):
    # Case a user is register but he didn't create any profile.
    profile, created = CustomerProfile.objects.get_or_create(user = request.user)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance = profile)
        if form.is_valid(): # validate the form
            form.save()
            messages.success(request, "Your profile has been updated")
            return redirect('home:index')
    else: # Display the form
        form = CustomerProfileForm(instance=profile)

    context ={
        'form':form
    }

    return render(request, 'profile.html', context)
