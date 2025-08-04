from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    data = {
        'title': "Landing Page' Dashboard",
    }

    return render(request, 'dashboard/index.html', data)