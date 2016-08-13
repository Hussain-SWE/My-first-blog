from django.shortcuts import render
from django.utils import timezone
from .models import post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect

#def post_list(request):
    #return render(request, 'blog/post_list.html', {})

def post_list(request):
    posts = post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    Post = get_object_or_404(post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': Post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    Post = get_object_or_404(post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=Post)
        if form.is_valid():
            Post = form.save(commit=False)
            Post.author = request.user
            Post.published_date = timezone.now()
            Post.save()
            return redirect('post_detail', pk=Post.pk)
    else:
        form = PostForm(instance=Post)
    return render(request, 'blog/post_edit.html', {'form': form})
