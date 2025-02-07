from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('',views.CreateView.as_view(),name='create'),
    path('list/', views.ListProductsView.as_view(), name='list'),
    path('detail/<int:pk>/', views.DetailProductView.as_view(), name='detail'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('delete/<int:pk>/', views.DeleteProductView.as_view(), name='delete'),
    path('create/', views.CreateProductView.as_view(), name='createProduct'),
]
