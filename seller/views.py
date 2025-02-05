from django.shortcuts import render
from django.views import View

# Create your views here.

class CreateView(View):
    template_name = 'seller/create.html'

    def setup(self, request, *args, **kwargs):
        
        return super().setup(request, *args, **kwargs)