from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .models import Blog, Blogger, Comment
from .forms import CommentForm, UserRegistrationForm, BloggerProfileForm
from django.utils import timezone
from django.contrib.auth import login
from django.contrib import messages
from .translation_utils import translate_text, detect_language
from django.http import JsonResponse

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a blogger profile for the new user
            Blogger.objects.create(user=user, bio="Welcome to my blog!")
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def index(request):
    """View function for home page of site."""
    num_blogs = Blog.objects.count()
    num_bloggers = Blogger.objects.count()
    
    context = {
        'num_blogs': num_blogs,
        'num_bloggers': num_bloggers,
    }
    
    return render(request, 'blog_app/index.html', context=context)

class BlogListView(generic.ListView):
    model = Blog
    template_name = 'blog_app/blog_list.html'
    context_object_name = 'blogs'
    ordering = ['-post_date']
    paginate_by = 5

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    # Handle translation request
    translated_content = None
    translated_title = None
    target_language = None
    
    # Detect the original language of the blog content
    original_language = detect_language(blog.content)
    
    if 'translate' in request.GET:
        target_lang = request.GET.get('to', None)
        # Only translate if the target language is different from the original
        if target_lang != original_language:
            translated_title, lang = translate_text(blog.title, target_lang)
            translated_content, target_language = translate_text(blog.content, target_lang)
    
    # Check if user liked the blog
    is_liked = False
    if request.user.is_authenticated:
        if blog.likes.filter(id=request.user.id).exists():
            is_liked = True
    
    context = {
        'blog': blog,
        'translated_title': translated_title,
        'translated_content': translated_content,
        'target_language': target_language,
        'original_language': original_language,
        'total_likes': blog.total_likes(),
        'is_liked': is_liked
    }
    
    return render(request, 'blog_app/blog_detail.html', context)

class BloggerListView(generic.ListView):
    model = Blogger
    template_name = 'blog_app/blogger_list.html'
    context_object_name = 'bloggers'
    paginate_by = 9  # Show 9 bloggers per page (3x3 grid)
    ordering = ['-user__date_joined']  # Order by newest members first

def blogger_detail(request, pk):
    blogger = get_object_or_404(Blogger, pk=pk)
    # Get the blogger's posts ordered by most recent first
    blogs = blogger.blog_set.order_by('-post_date')
    return render(request, 'blog_app/blogger_detail.html', {
        'blogger': blogger,
        'blogs': blogs
    })

@login_required
def edit_profile(request):
    try:
        blogger = Blogger.objects.get(user=request.user)
    except Blogger.DoesNotExist:
        blogger = Blogger.objects.create(user=request.user, bio="Welcome to my blog!")

    if request.method == 'POST':
        form = BloggerProfileForm(request.POST, request.FILES, instance=blogger)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('blogger-detail', pk=blogger.pk)
    else:
        form = BloggerProfileForm(instance=blogger)
    return render(request, 'blog_app/profile_edit.html', {'form': form})

@login_required
def create_comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.post_date = timezone.now()
            comment.save()
            return redirect('blog-detail', pk=blog.pk)
    else:
        form = CommentForm()
    return render(request, 'blog_app/comment_form.html', {'form': form, 'blog': blog})

@login_required
def like_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    # Check if the user already liked the post
    if blog.likes.filter(id=request.user.id).exists():
        # User already liked the post, so remove the like
        blog.likes.remove(request.user)
        liked = False
    else:
        # User hasn't liked the post, so add the like
        blog.likes.add(request.user)
        liked = True
    
    # Return JSON response for AJAX
    return JsonResponse({
        'liked': liked,
        'total_likes': blog.total_likes()
    })

class BlogCreate(LoginRequiredMixin, generic.CreateView):
    model = Blog
    template_name = 'blog_app/blog_form.html'
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        # Get or create a blogger profile for the user
        blogger, created = Blogger.objects.get_or_create(
            user=self.request.user,
            defaults={'bio': "Welcome to my blog!"}
        )
        form.instance.author = blogger
        form.instance.post_date = timezone.now()
        return super().form_valid(form)

class BlogUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    template_name = 'blog_app/blog_form.html'
    fields = ['title', 'content', 'image']

    def get_success_url(self):
        return reverse_lazy('blog-detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.user != self.request.user:
            return redirect('blogs')
        return super().dispatch(request, *args, **kwargs)

class BlogDelete(LoginRequiredMixin, generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('blogs')
    template_name = 'blog_app/blog_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author.user != self.request.user:
            return redirect('blogs')
        return super().dispatch(request, *args, **kwargs)
