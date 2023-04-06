from django.urls import path

from . import views

app_name = "exoplanet"
urlpatterns = [
    # homepage
    path("", views.index, name="index"),

    # user management urls
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),

    # exoplanet API
    path('exoplanets/', views.ExoplanetListCreateView.as_view(), name='exoplanet_list_create'),
    path('exoplanets/<int:pk>/', views.ExoplanetRetrieveUpdateDestroyView.as_view(), name='exoplanet_retrieve_update_destroy'),

]