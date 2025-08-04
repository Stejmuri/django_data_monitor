from django.shortcuts import render

# Create your views here.
def index(request):
    """
    Render the dashboard index page.
    """
    return render(request, 'dashboard/base.html')