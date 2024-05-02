from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', views.single_post_page, name='single_page'),
    path('tag/<slug:tag>/', views.TagViewList.as_view(), name='tag_boy_post'),
]
