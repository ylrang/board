from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from .models import Post, Document
from .forms import PostForm, DocumentForm
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.views.generic import CreateView

# Create your views here.
"""def index(request):
    page = request.GET.get('page', '1')
    posts = Post.objects.order_by('-created')
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(page)
    return render(request, 'cloud/jobs.html', {'posts': page_obj})
"""
"""
def create_post(request):
    formset_class = modelformset_factory(Document, form=DocumentForm, extra=0)

    if request.method == 'POST':

        postForm = PostForm(request.POST)
        formset = formset_class(request.POST, request.FILES, queryset=Document.objects.none())
        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.created = timezone.now()
            post_form.save()
            for form in formset.cleaned_data:
                if form:
                    file = form['files']
                    document = Document(post=post_form, attached=file, filename=file.name, content_type=file.content_type, size=file.size)
                    document.save()
            return redirect(index)
    else:
        postForm = PostForm()
        formset = formset_class(queryset=Document.objects.none())
    return render(request, 'cloud/job_form.html', {'post': postForm, 'formset': formset})
"""
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

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'category', 'institute']
    template_name = 'cloud/job_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.updated = timezone.now()
        response = super().form_valid(form)
        
        if self.request.FILES:
            for file in self.request.FILES.getlist('files'):
                file = Document(post=self.object, attached=file, filename=file.name, content_type=file.content_type, size=file.size)
                file.save()
        return response


def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('index')
    

from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

def download_file(request, pk):
    file = Document.objects.get(pk=pk)
    file_path = file.attached.path
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_path, 'rb'), content_type=file.content_type)
    response['Content-Disposition'] = f'attachement; filename={file.filename}'
    
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
