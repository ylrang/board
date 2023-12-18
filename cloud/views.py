from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator

# Create your views here.
"""def index(request):
    page = request.GET.get('page', '1')
    posts = Post.objects.order_by('-created')
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(page)
    return render(request, 'cloud/jobs.html', {'posts': page_obj})
"""


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created = timezone.now()
            if request.FILES:
                post.document = request.FILES['document']
            post.save()
            return render(request, 'cloud/job_details.html', {'post': post})
    else:
        form = PostForm()
        return render(request, 'cloud/job_form.html', {'form': form})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'cloud/job_details.html', {'post' : post})

def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated = timezone.now()
            post.save()
            return render(request, 'cloud/job_details.html', {'post': post})
    else:
        form = PostForm(instance=post)
        return render(request, 'cloud/job_form.html', {'post' : post, 'form' : form})
        

def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('index')
    

from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

def download_file(request, pk):
    object = get_object_or_404(Post, pk=pk)
    file_path = object.document.path
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_path, 'rb'), content_type=object.get_filetype())
    response['Content-Disposition'] = f'attachement; filename={object.get_filename()}'
    
    return response

def index(request):
    page = request.GET.get('page', '1')
    type = request.GET.get('type', '1')
    kw = request.GET.get('kw', '')
    inst = request.GET.get('institute', '0')
    cat = request.GET.get('category', '0')
    sort = request.GET.get('sort', '1')
    if sort == '1':
        posts = Post.objects.order_by('-created')
    elif sort == '2':
        posts = Post.objects.order_by('created')
    else:
        posts = Post.objects.order_by('-created')
    if kw:
        if type == '1':
            posts = posts.filter(Q(title__icontains=kw)).distinct()
        elif type == '2':
            posts = posts.filter(Q(content__icontains=kw)).distinct()
        elif type == '3':
            posts = posts.filter(Q(title__content__icontains=kw)).distinct()
        elif type == '4':
            posts = posts.filter(Q(author__icontains=kw)).distinct()
    if inst == '0':
        posts = posts
    else:
        posts = posts.filter(institute=inst)
    if cat == '0':
        posts = posts
    else:
        posts = posts.filter(category=cat)
    
    
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(page)
    
    return render(request, 'cloud/jobs.html', {'posts': page_obj, 'page': page})
