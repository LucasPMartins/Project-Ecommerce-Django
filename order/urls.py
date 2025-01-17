from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('payment/<int:pk>',views.PaymentView.as_view(), name='payment'),
    path('saveorder/', views.SaveOrderView.as_view(), name='save'),
    path('detail/<int:pk>', views.DetailOrderView.as_view(), name='detail'),
    path('list/', views.ListOrderView.as_view(), name='list'),
]
