import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

from google_auth_oauthlib.flow import Flow

from .forms import DoctorSignupForm, PatientSignupForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from bookings.email_service import send_email_notification

User = get_user_model()

def home(request):
    return render(request, 'accounts/home.html')


@login_required
def google_auth(request):
    request.session['google_auth_user_id'] = request.user.id
    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'credentials.json'),
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri='http://localhost:8000/oauth2callback/'
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)



def oauth2callback(request):
    user_id = request.session.get('google_auth_user_id')

    if not user_id:
        messages.success(request, "Google Calendar connected successfully.")
        return redirect('login')  # fallback only

    user = User.objects.get(id=user_id)

    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri='http://localhost:8000/oauth2callback/'
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials

    user.google_token = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }
    user.save()

    request.session.pop('google_auth_user_id', None)

    messages.success(request, "Google Calendar connected successfully 🎉")

    if user.role == 'doctor':
        return redirect('doctor_dashboard')
    else:
        return redirect('patient_dashboard')


def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            send_email_notification(
                email_type="SIGNUP_WELCOME",
                to_email=user.email,
                username=user.username
            )
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        form = DoctorSignupForm()
    return render(request, 'accounts/signup_doctor.html', {'form': form})



def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email_notification(
                email_type="SIGNUP_WELCOME",
                to_email=user.email,
                username=user.username
            )
            login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientSignupForm()
    return render(request, 'accounts/signup_patient.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.role == 'doctor':
                return redirect('doctor_dashboard')
            return redirect('patient_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def doctor_dashboard(request):
    return render(request, 'accounts/doctor_dashboard.html')


@login_required
def patient_dashboard(request):
    return render(request, 'accounts/patient_dashboard.html')

def signup_choice(request):
    return render(request, 'accounts/signup_choice.html')
