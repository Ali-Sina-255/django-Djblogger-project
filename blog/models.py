from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.urls import reverse


class Post(models.Model):
    DRAFT_CHOICES = 'Draft'
    PUBLISHED_CHOICES = 'Published'
    POST_CHOICES = (
        (DRAFT_CHOICES, "Draft"),
        (PUBLISHED_CHOICES, "Published"),
    )
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post_author')
    content = models.TextField()
    status = models.CharField(
        max_length=30, choices=POST_CHOICES, default=DRAFT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    tags = TaggableManager()
    
    def get_absolute_url(self):
        return reverse('single_page', args=[self.slug])