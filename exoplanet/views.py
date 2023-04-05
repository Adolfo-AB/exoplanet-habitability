from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import generics

from exoplanet.models import Exoplanet
from exoplanet.serializers import ExoplanetSerializer


# Home Page View
def index(request):
    return render(request, 'exoplanet/index.html')


# User Management Views
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'exoplanet/register.html'
    success_url = reverse_lazy('exoplanet:index')


class UserLoginView(LoginView):
    template_name = 'exoplanet/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('exoplanet:index')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('exoplanet:index')


# Exoplanet API Views
class ExoplanetListCreateView(generics.ListCreateAPIView):
    queryset = Exoplanet.objects.all()
    serializer_class = ExoplanetSerializer


class ExoplanetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exoplanet.objects.all()
    serializer_class = ExoplanetSerializer
