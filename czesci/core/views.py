from django.shortcuts import render

# Create your views here.

def home(request):
    """Render main landing page"""
    return render(request, "core/index.html")
