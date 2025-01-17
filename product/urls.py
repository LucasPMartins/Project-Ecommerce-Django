from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('<slug>', views.ProductDetailView.as_view(), name='detail'),
    path('addtocart/', views.AddToCartView.as_view(), name='addtocart'),
    path('removefromcart/', views.RemoveFromCartView.as_view(), name='removefromcart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('resume/', views.ResumeView.as_view(), name='resume'),
    path('search/', views.SeachProductView.as_view(), name='search'),
]
