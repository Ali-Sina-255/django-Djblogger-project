from django.shortcuts import render
from . models import Post
from django.views.generic import ListView
from django.http import HttpResponse


class HomeView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    
def home(request):
    return render(request, 'blog/index.html')
