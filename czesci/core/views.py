from django.shortcuts import render

# Create your views here.

def home(request):
    """Render main landing page"""
    return render(request, "core/index.html")

def how_it_works(request):
    """Render 'How It Works' page"""
    return render(request, "core/how_it_works.html")
