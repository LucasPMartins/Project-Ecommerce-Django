from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse

class PaymentView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Payment')

class CloseOrderView(View):
    pass

class DetailOrderView(View):
    pass