from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from contacts.models import Contact

from accounts.api.serializers import UserSerializer
from contacts.serializers import ContactSerializer


@api_view(['POST'])
def register(request):
    # Get form values
    errors = {}
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    print(request.POST.get('username'))

    # Check if passwords match
    if password == password2:
        # Check username
        if User.objects.filter(username=username).exists():
            errors['error'] = 'That username is taken'
            return redirect('register')
        else:
            if User.objects.filter(email=email).exists():
                errors['error'] = 'That email is being used'
                return Response(errors)
            else:
                # Looks good
                user = User.objects.create_user(username=username, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                errors['success'] = 'You are now registered and can log in'
                return Response(errors)
    else:
        errors['error'] = 'Passwords do not match'
        return Response(errors)


@api_view(['GET'])
def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': ContactSerializer(user_contacts, many=True).data
    }

    return JsonResponse(context)
