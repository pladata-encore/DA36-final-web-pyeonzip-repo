from django.contrib import auth,messages
from django.shortcuts import render, redirect
from django.http import JsonResponse

# from oauth.entity.models import UserForm
# from oauth.service.uauth_service import UAuthServiceImpl

# oauth_service=OAuthServiceImpl.get_instance()

def index(request):
    pass

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out.')

