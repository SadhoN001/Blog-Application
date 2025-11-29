from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Tag
from .forms import CommentForm, PostForm, TagForm, UserRegisterForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
def post_list(request):
    query = request.GET.get('q')
    tag = request.GET.get('tag')
    posts = Post.objects.filter(status = 'Published').order_by('-created_at')
    if query:
        posts = posts.filter(Q(title__icontains = query) | Q(content__icontains = query))
        
    if tag:
        posts = posts.filter(tags__slug = tag)
    paginator = Paginator(posts, 4)
    page_number =  request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.all()
    context = {
        'search_query' : query,
        'page_obj' : page_obj,
        'tag': tag,
        'tags': tags
    }
    return render(request, 'post_list.html', context)

def post_details(request, slug):
    post = get_object_or_404(Post, slug = slug, status = 'Published')
    comments = post.comments.all() # related name from Comment
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return redirect('post_details', slug = post.slug)
        else:
            return redirect('login')
    else:
        form = CommentForm()
    context = {
        'form' : form,
        'comments' : comments,
        'post': post,
    }
    return render(request, 'post_detail.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id= post_id)
    if post.liked_user.filter(id = request.user.id).exists():
        post.liked_user.remove(request.user)
    else:
        post.liked_user.add(request.user)
    return redirect('post_details', slug = post.slug)

class TagCreateView(SuccessMessageMixin, LoginRequiredMixin ,CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'create_tag.html'
    success_url = reverse_lazy('post_create')
    success_message = "Tag Created Succesfull"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

def post_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug = slug)
    posts = tag.post_set.filter(status = 'Published')
    return render(request, 'tag_posts.html', {'tag':tag, 'posts':posts})

@login_required
def deshboard(request):
    posts = Post.objects.filter(author = request.user).order_by('-created_at')
    paginator = Paginator(posts, 7)
    page_number =  request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard.html', {'posts':posts, 'page_obj': page_obj})

class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView ):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('deshboard')
    success_message = "Post Created succesfull"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        # messages.success(self.request, "Post Create Successfully !!")
        return super().form_valid(form) 
   
class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('deshboard')
    success_message = "Post Updated succesfull"
    
    def test_func(self): # user can access control
        return self.request.user == self.get_object().author

    
class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('deshboard')
    success_message = "Post Deleted succesfull"
    
    def test_func(self):
        return self.request.user == self.get_object().author
    

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successfully !!")
            return redirect('post_list')
    else:
        form = UserRegisterForm()
        
    return render(request, 'register.html', {'form': form})
    

