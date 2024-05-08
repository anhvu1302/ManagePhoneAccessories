from pyexpat import model
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import AuthenticationForm
from django.shortcuts import redirect
from .forms import IdentifyForm
from .forms import RegistrationForm
from .forms import RecoveryForm
from .forms import SendSuccess
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
# Create your views here.
def index(request):
    return render(request, "pages/index.html")


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
         
       
                return redirect('index') 
        else:
            
                return render(request, 'pages/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})





def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect('/login')
    return render(request, 'pages/register.html', {'form': form})


def identify(request):
    if request.method == 'POST':
        form = IdentifyForm(request.POST)
        if form.is_valid():
            try:
                form.send_password_reset_email(request)
                return render(request, 'pages/success.html')
            except ValidationError as e:
                form.add_error('email', e)
    else:
        form = IdentifyForm()
    return render(request, 'pages/identify.html', {'form': form})

def recovery(request, uidb64, token):
    if request.method == 'POST':
        form = RecoveryForm(data=request.POST, uidb64=uidb64, token=token)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            form.save(new_password)
      
        return redirect('login')  
    else:
        form = RecoveryForm(uidb64=uidb64, token=token)
    return render(request, 'pages/recovery.html', {'form': form})