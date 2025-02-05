from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('',views.CreateView.as_view(),name='create'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
]
