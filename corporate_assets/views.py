from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework import status
from .serializers import *
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login as Login_process 


# Create your views here.



#API

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        data = request.data.copy()
        is_new_company_admin = data.pop('new_company', False)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            date_of_birth = data.pop('date_of_birth', None)
            if is_new_company_admin=='on':
                company_data = {
                    'name': data.get('cname'),
                    'location': data.get('location'),
                    'license_id': data.get('license_id')
                }
                company_serializer = CompanySerializer(data=company_data)
                if company_serializer.is_valid():
                    company_serializer.save()
                    company = company_serializer.instance
                    user_profile_data = {
                        'user': user.pk,
                        'date_of_birth': date_of_birth,
                        'joining_date': data.get('joining_date',None),
                        'nationality': data.get('nationality', None),
                        'branch': None, 
                        'designation': 'Admin',
                        'company': company.pk,
                        'is_company_admin': True,
                        'is_branch_manager': False
                    }
                    user_profile_serializer = UserProfileSerializer(data=user_profile_data)
                    print(user_profile_serializer)
                    if user_profile_serializer.is_valid():
                        user_profile_serializer.save()
                        return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED)
                    return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_profile_data = {
                    'user': user.pk,
                    'date_of_birth': date_of_birth,
                    'joining_date': data.get('joining_date',None),
                    'nationality': data.get('nationality',None),
                    'branch': None, 
                    'designation': 'User',
                    'company': data.get('company_id'),
                    'is_company_admin': False,
                    'is_branch_manager': False
                }
                user_profile_serializer = UserProfileSerializer(data=user_profile_data)
                if user_profile_serializer.is_valid():
                    user_profile_serializer.save()
                    return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED)
                return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            Login_process(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def company_assets_list(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    company_id = user_profile.company_id
    devices = Device.objects.filter(company_id=company_id)
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_company_ID(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    company_id = user_profile.company_id
    return Response(company_id)

@api_view(['POST'])
def add_asset(request):
    if request.method == 'POST':
        name = request.data.get('name')
        company_id = request.data.get('company_id')

 
        device = Device.objects.create(name=name, company_id=company_id)

        serializer = DeviceSerializer(device)

        return Response(serializer.data)
    else:
        return Response(status=405)



@api_view(['GET'])
def retrieve_asset(request, asset_id):
    try:
        device = Device.objects.get(pk=asset_id)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = DeviceSerializer(device)
    return Response(serializer.data)

@api_view(['PUT'])
def update_asset(request, asset_id):
    try:
        device = Device.objects.get(pk=asset_id)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = DeviceSerializer(device, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_asset(request, asset_id):
    try:
        device = Device.objects.get(pk=asset_id)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    device.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




#Views

def home(request):
    return render(request,'home.html')

def register(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

@login_required
def dashboard(request):
    user = request.user 
    context = {
        'user': user,
    }
    return render(request, 'dashboard.html', context)


def logout(request):
    logout(request)
    return redirect('/login')