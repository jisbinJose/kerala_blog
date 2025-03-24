from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.blog_detail, name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>', views.blogger_detail, name='blogger-detail'),
    path('blog/<int:pk>/comment/', views.create_comment, name='blog-comment'),
    path('blog/create/', views.BlogCreate.as_view(), name='blog-create'),
    path('blog/<int:pk>/update/', views.BlogUpdate.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete/', views.BlogDelete.as_view(), name='blog-delete'),
    path('register/', views.register, name='register'),
    path('profile/edit/', views.edit_profile, name='profile-edit'),
]
