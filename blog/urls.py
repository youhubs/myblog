from django.urls import path

from . import views

app_name = "posts"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('categories/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('archives/<int:year>/<int:month>/',
         views.ArchiveView.as_view(), name='archive'),
    path('tags/<int:pk>', views.TagView.as_view(), name='tag'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('search/', views.search, name='search'),
    path('full_view/', views.FullView.as_view(), name='full_view'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
