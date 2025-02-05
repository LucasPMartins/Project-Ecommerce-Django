from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('',views.CreateView.as_view(),name='create'),
    path("list/", views.ListProductsView.as_view(), name="list"),
    path("advertise/", views.AdvertiseView.as_view(), name="advertise"),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
]
