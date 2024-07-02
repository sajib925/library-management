from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import  logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from decimal import Decimal
from django.core.mail import send_mail
from decimal import Decimal
from books.models import Borrowing




class RegisterView(FormView):
    template_name = 'register.html'
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('user_login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Account Created Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = 'register.html'
    def get_success_url(self):
        return reverse_lazy('homepage')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    

@login_required
def profile(request):
    profile = request.user.profile
    borrowings = Borrowing.objects.filter(user=request.user)
    return render(request, 'profile.html', {'profile': profile,'borrowings': borrowings})


@login_required
def deposit(request):
    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        try:
            amount = Decimal(amount_str)
            if amount > 0:
                profile = request.user.profile
                profile.balance += amount
                profile.save()
                messages.success(request, f'Deposit of {amount} successfully added to your account')
                
                send_mail(
                    'Deposit Successful',
                    f'Hi {request.user.username},\n\nYour deposit of {amount} has been successfully added to your account. Your new balance is {profile.balance}.',
                    'from@example.com',
                    [request.user.email],
                    fail_silently=False,
                )
                
            else:
                messages.error(request, 'Deposit amount must be greater than zero')
        except ValueError:
            messages.error(request, 'Invalid amount')
        return redirect('profile')
    return render(request, 'deposit.html')


# @login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')