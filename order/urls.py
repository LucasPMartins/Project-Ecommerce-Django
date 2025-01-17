from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('',views.PaymentView.as_view(), name='payment'),
    path('closeorder/', views.CloseOrderView.as_view(), name='closeorder'),
    path('detail/', views.DetailOrderView.as_view(), name='detail'),
]
