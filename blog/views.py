from django.shortcuts import render
from . models import Post
from django.views.generic import ListView
from django.http import HttpResponse


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
    except Post.DoesNotExist:
        return HttpResponse(f'post with is slug {slug} is not found!')
    context = {
        "post":post
    }
    return render(request, 'blog/single_Post.html', context)