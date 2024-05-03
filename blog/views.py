from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . models import Post
from django.views.generic import ListView
from django.http import HttpResponse
from .forms import PostSearchForm
from django.db.models import Q

class HomeView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_template_names(self):
        if self.request.htmx:
            return "components/post-list-element.html"
        return 'blog/index.html'
    
def home(request):
    return render(request, 'blog/index.html')


def single_post_page(request, slug):
    try:
        post = Post.objects.get(slug=slug, status="Published")
        related = Post.objects.filter(author = post.author)[:5]
    except Post.DoesNotExist:
        return HttpResponse(f'post with is slug {slug} is not found!')
    context = {
        "post":post,
        "related": related
    }
    return render(request, 'blog/single_Post.html', context)

class TagViewList(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        return Post.objects.filter(tags__name__in=[self.kwargs['tag']])
    def get_template_names(self):
        if self.request.htmx:
            return "components/post-list-tag.html"
        return 'blog/tags.html'
    
    def get_context_data(self, **kwargs):
        context = super(TagViewList, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context
        
        
class SearchPost(ListView):
    model  = Post
    context_object_name = 'posts'
    paginate_by = 10
    from_class = PostSearchForm
    
    def get_queryset(self):
        form = self.from_class(self.request.GET)
        if form.is_valid():
            return Post.objects.filter(title__icontains=form.cleaned_data['q'])
        return []
    def get_template_names(self):
        if self.request.htmx:
            return "components/post-list-element-search.html"
        return 'blog/search.html'
    

def search_post(request, *args, **kwargs):
    query = request.GET.get("q")
    qs = Post.objects.all()
    if query is not None:
        lookups = Q(title__icontains=query) | Q(content__icontains=query) | Q(
            subtitle__icontains=query
        )
        qs = Post.objects.filter(lookups)
    context = {
        'posts': qs
    }
    if request.htmx:
        return render(request, 'components/post-list-element-search.html')
    return render(request, 'blog/search.html', context)