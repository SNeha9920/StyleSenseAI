from django.shortcuts import render
import json
from json import dumps
from urllib.parse import urlencode

import subprocess, functools, platform
import os

from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models.functions import ExtractMonth, ExtractYear
from django.forms import model_to_dict
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework import status
from datetime import datetime, time, timedelta
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import requests
from django.db import transaction
from django.db.models import Q
from uuid import uuid4
from urllib3.exceptions import InsecureRequestWarning
from django.utils.html import escape

from collections import defaultdict

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

import json
from uuid import uuid4
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view

from .models import (
    user_login, Tokens, UserProfile, UserSettings,
    WardrobeItem, OutfitCollection, SkinAnalysis,
    VirtualTryOn, AIStylistSession, ChatMessage
)
from .serializers import userLoginSerializer, TokenSerializer

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import user_login, UserProfile

from django.shortcuts import render, get_object_or_404
from .models import SkinAnalysis

# ==========================================
# AUTHENTICATION & SESSION HELPER
# ==========================================

def get_current_user(request):
    """Retrieve logged in user from session if available."""
    user_data = request.session.get('userobj')
    if user_data and 'id' in user_data:
        try:
            return user_login.objects.get(id=user_data['id'])
        except user_login.DoesNotExist:
            return None
    return None


def get_skin_analysis_detail(request, analysis_id):
    fastapi_url = f"{settings.FASTAPI_BASE_URL}/skin-analysis/{analysis_id}"
    
    # Pass authorization header if using tokens
    token = request.session.get('auth_token')
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        response = requests.get(fastapi_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return render(request, 'skin_analysis_detail.html', {'analysis': response.json()})
    except requests.exceptions.RequestException:
        pass

    return redirect('skin_analysis')


def get_skin_analysis_detail(request, analysis_id):
    user_id = request.session.get('user_id')
    analysis = get_object_or_404(SkinAnalysis, id=analysis_id, user_id=user_id)
    
    return render(request, 'skin_analysis_detail.html', {'analysis': analysis})


def skin_analysis_view(request, analysis_id=None):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, "Please log in to access Skin Analysis.")
        return redirect('login')

    # If an ID is provided, load specific analysis; otherwise load the latest record
    if analysis_id:
        analysis = get_object_or_404(SkinAnalysis, id=analysis_id, user_id=user_id)
    else:
        analysis = SkinAnalysis.objects.filter(user_id=user_id).order_by('-created_at').first()

    # Load history for sidebar/previous scans list
    history = SkinAnalysis.objects.filter(user_id=user_id).order_by('-created_at')[:5]

    context = {
        'analysis': analysis,
        'history': history,
    }
    return render(request, 'skin_analysis.html', context)


@api_view(['POST', 'GET'])
# @TokenChecker
def index(request):
    return render(request, 'index.html')


@csrf_exempt
@api_view(['POST', 'GET'])
def register(request):
    if request.method == 'POST':
        full_name = request.data.get('fullName', '').strip()
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '').strip()

        if not email or not password or not full_name:
            return JsonResponse({"status": False, "message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if user_login.objects.filter(email=email).exists():
            return JsonResponse({"status": False, "message": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        name_parts = full_name.split(' ', 1)
        firstname = name_parts[0]
        lastname = name_parts[1] if len(name_parts) > 1 else ''

        with transaction.atomic():
            # Pass explicit Python booleans (True/False), not string literals ("true"/"false")
            user = user_login.objects.create(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=make_password(password),
                created_at=timezone.now()
            )
            # Create default Profile and Settings
            UserProfile.objects.create(user=user)
            UserSettings.objects.create(user=user)

        messages.success(request, "Account created successfully! Please log in.")
        #return JsonResponse({"status": True, "message": "Registration successful!"}, status=status.HTTP_201_CREATED)
        return redirect('login')

    return render(request, 'register.html')


def TokenChecker(Wrapped):
    def wrapper(*args, **kwargs):
        request = args[0]

        try:
            tokenval = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            userid = request.META['HTTP_AUTHORIZATION'].split(' ')[2]
        except (KeyError, IndexError):
            print(request.headers.get('Authorization'))
            return HttpResponse('<h1>Unauthorized(401)</h1>', status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = user_login.objects.get(id=userid)
        except user_login.DoesNotExist:
            return HttpResponse('<h1>Unauthorized(401)</h1>', status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = Tokens.objects.get(user=user)
        except Tokens.DoesNotExist:
            return HttpResponse('<h1>Unauthorized(401)</h1>', status=status.HTTP_401_UNAUTHORIZED)

        # VALID LOGIN
        if token.value == tokenval and token.valid_upto > timezone.now():
            return Wrapped(*args, **kwargs)

        else:
            return HttpResponse('<h1>Token Expired(401)</h1>', status=status.HTTP_401_UNAUTHORIZED)

    return wrapper


# Login User Page
@csrf_exempt
@api_view(['POST', 'GET'])
def userLogin(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return JsonResponse({"status": False, "Desc": "Couldn't get data from site"})

        try:
            userobj = user_login.objects.get(email=email)
        except:
            messages.error(request, 'Invalid Login')
            return render(request, 'login.html')
            #return JsonResponse({"Message": "Invalid Login"}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = userLoginSerializer(userobj)

        if check_password(password, userobj.password):
            # Login Accepted
            try:
                token = Tokens.objects.get(user=userobj, logged_out_at__isnull=True)
                token_updated = TokenSerializer(token).data
                token_updated['logged_out_at'] = timezone.now()
                token_sez = TokenSerializer(token, data=token_updated)
                if token_sez.is_valid():
                    token_sez.save()
                else:
                    return redirect('logout')
            except Tokens.DoesNotExist:
                pass
            token_code = str(uuid4())
            Tokens.objects.create(value=token_code, valid_upto=timezone.now() + timedelta(minutes=40), user=userobj)
            request.session['userobj'] = user_serializer.data
            msg = "{} {} Logged In Successfully!".format(userobj.firstname, userobj.lastname)
            messages.success(request, msg)
            return redirect('dashboard')

        else:
            # Bad Login
            messages.error(request, 'Email or Password did not match')
            print('Email or Password did not match')
            return render(request, 'login.html')
            #return JsonResponse({"status": False, "Desc": "Username or Password did not match"})
    elif request.method == 'GET':
        # print(request.session.get('userobj'))
        return render(request, 'login.html')
    else:
        # Wrong Request method
        return JsonResponse({"status": False, "Desc": "Wrong Request Method"})




@api_view(['POST', 'GET'])
def Logout(request, userid):
    try:
        userobj = user_login.objects.get(id=userid)
        tokenobj = Tokens.objects.get(user=userobj, logged_out_at__isnull=True)
        tokenobj.logged_out_at = timezone.now()
        tokenobj.save()
    except (user_login.DoesNotExist, Tokens.DoesNotExist):
        pass

    request.session['userobj'] = {}
    messages.success(request, "User Logged Out")
    return redirect('login')


# ==========================================
# PAGE VIEWS & API ENDPOINTS
# ==========================================

@api_view(['GET'])
def dashboard(request):
    user = get_current_user(request)
    context = {'user': user}
    print()
    return render(request, 'dashboard.html', context)


@api_view(['POST', 'GET'])
# @TokenChecker
def skinanalysis(request):
    return render(request, 'skin-analysis.html')


@api_view(['POST', 'GET'])
# @TokenChecker
def virtualtryon(request):
    return render(request, 'virtual-try-on.html')


@api_view(['POST', 'GET'])
# @TokenChecker
def aistylist(request):
    return render(request, 'ai-stylist.html')


@api_view(['POST', 'GET'])
# @TokenChecker
def wardrobe(request):
    return render(request, 'wardrobe.html')


@api_view(['POST', 'GET'])
# @TokenChecker
def history(request):
    return render(request, 'history.html')


"""@login_required
def profile_view(request):
    # Retrieve user and profile records for the logged-in user
    # If using custom user_login table:
    user_id = request.session.get('user_id')  # or request.user.id if using standard Django auth
    user = user_login.objects.get(id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        # Handle form submission / saving changes
        user.firstname = request.POST.get('firstname', user.firstname)
        user.lastname = request.POST.get('lastname', user.lastname)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', getattr(user, 'phone', ''))
        user.save()

        profile.height = request.POST.get('height', profile.height)
        profile.weight = request.POST.get('weight', profile.weight)
        profile.body_type = request.POST.get('body_type', profile.body_type)
        profile.fit_preference = request.POST.get('fit_preference', profile.fit_preference)
        profile.skin_tone = request.POST.get('skin_tone', profile.skin_tone)
        profile.skin_type = request.POST.get('skin_type', profile.skin_type)
        profile.skin_concerns = request.POST.get('skin_concerns', profile.skin_concerns)
        profile.chest = request.POST.get('chest', profile.chest)
        profile.waist = request.POST.get('waist', profile.waist)
        profile.hip = request.POST.get('hip', profile.hip)
        profile.shoulder = request.POST.get('shoulder', profile.shoulder)
        profile.sleeve_length = request.POST.get('sleeve_length', profile.sleeve_length)
        profile.shoe_size = request.POST.get('shoe_size', profile.shoe_size)
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    context = {
        'user_data': user,
        'profile': profile,
    }
    return render(request, 'profile.html', context)
"""

@login_required
def profile_view(request):
    # 1. Fetch user ID from session or request.user
    user_id = request.session.get('user_id') or getattr(request.user, 'id', None)

    if not user_id:
        # If no logged-in user is found, redirect to login
        messages.error(request, "Please log in to view your profile.")
        return redirect('login')

    # 2. Fetch the logged-in user and their profile
    try:
        user = user_login.objects.get(id=user_id)
    except user_login.DoesNotExist:
        messages.error(request, "User record not found.")
        return redirect('login')

    # Fetch or automatically create the profile for this user
    profile, created = UserProfile.objects.get_or_create(user=user)

    # 3. Handle Form POST
    if request.method == 'POST':
            # Update user fields
            user.firstname = request.POST.get('firstname', user.firstname)
            user.lastname = request.POST.get('lastname', user.lastname)
            user.email = request.POST.get('email', user.email)
            user.save()

            # Update profile fields
            profile.phone = request.POST.get('phone', profile.phone)
            profile.location = request.POST.get('location', profile.location)

            # Handle Date of Birth safely
            dob_val = request.POST.get('dob')
            if dob_val:
                profile.dob = dob_val

            # Handle Numeric Fields safely
            height_val = request.POST.get('height')
            weight_val = request.POST.get('weight')
            profile.height = height_val if height_val != '' else None
            profile.weight = weight_val if weight_val != '' else None

            # Select & Other profile fields
            profile.body_type = request.POST.get('body_type', profile.body_type)
            profile.fit_preference = request.POST.get('fit_preference', profile.fit_preference)
            profile.skin_tone = request.POST.get('skin_tone', profile.skin_tone)
            profile.skin_type = request.POST.get('skin_type', profile.skin_type)
            profile.skin_concerns = request.POST.get('skin_concerns', profile.skin_concerns)
            
            # Measurements
            profile.chest = request.POST.get('chest', profile.chest)
            profile.waist = request.POST.get('waist', profile.waist)
            profile.hip = request.POST.get('hip', profile.hip)
            profile.shoulder = request.POST.get('shoulder', profile.shoulder)
            profile.sleeve_length = request.POST.get('sleeve_length', profile.sleeve_length)
            profile.shoe_size = request.POST.get('shoe_size', profile.shoe_size)

            profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')

    # 4. Pass data to template
    context = {
        'user_data': user,
        'profile': profile,
    }
    return render(request, 'profile.html', context)

@csrf_exempt
@api_view(['GET', 'POST'])
def profile(request):
    user = get_current_user(request)
    user_profile, _ = UserProfile.objects.get_or_create(user=user) if user else (None, False)

    if request.method == 'POST' and user_profile:
        user_profile.phone = request.data.get('phone', user_profile.phone)
        user_profile.location = request.data.get('location', user_profile.location)
        user_profile.height_cm = request.data.get('height_cm') or user_profile.height_cm
        user_profile.weight_kg = request.data.get('weight_kg') or user_profile.weight_kg
        user_profile.body_type = request.data.get('body_type', user_profile.body_type)
        user_profile.fit_preference = request.data.get('fit_preference', user_profile.fit_preference)
        user_profile.skin_tone = request.data.get('skin_tone', user_profile.skin_tone)
        user_profile.skin_type = request.data.get('skin_type', user_profile.skin_type)
        user_profile.skin_concerns = request.data.get('skin_concerns', user_profile.skin_concerns)
        user_profile.chest_cm = request.data.get('chest_cm') or user_profile.chest_cm
        user_profile.waist_cm = request.data.get('waist_cm') or user_profile.waist_cm
        user_profile.hip_cm = request.data.get('hip_cm') or user_profile.hip_cm
        user_profile.save()

        messages.success(request, "Profile updated successfully!")
        return JsonResponse({"status": True, "message": "Profile updated."})

    return render(request, 'profile.html', {'user': user, 'profile': user_profile})


@api_view(['POST', 'GET'])
# @TokenChecker
def settings(request):
    return render(request, 'settings.html')

