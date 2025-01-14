from django.urls import path
from . import views

app_name = 'product'
# produto:
#     '' (lista de produtos)
#     <slug> detalhes do produto
#     addtocart
#     removefromcart
#     cart
#     finalizar
urlpatterns = [
    path('', views.ListProduct.as_view(), name='list'),
]
