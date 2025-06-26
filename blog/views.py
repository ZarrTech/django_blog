from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.views.generic import ListView
from .form import EmailPostForm
from django.http import Http404
from django.core.mail import send_mail
from .models import Post
# Create your views here.
def post_list(request):
    post_list = Post.published_manager.all()
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page', 1)
    try:
      post = paginator.page(page_number)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'post': post})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post,
    published__year=year,
    published__month=month,
    published__day=day)
    return render(request, 'blog/post/details.html', {'post': post})

class PostListView(ListView):
    queryset = Post.published_manager.all()
    context_object_name = 'post'
    paginate_by = 2
    template_name = 'blog/post/list.html'
    
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent =False
    if request.method == 'POST':
       form = EmailPostForm(request.POST)
       if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (f"{cd['name']} ({cd['email']}) "f"recommends you read {post.title}")
            message = (f"Read {post.title} at {post_url}\n\n" 
                       f"{cd['name']}\'s comments: {cd['comments']}")
            send_mail(
            subject=subject,
            message=message,
            from_email= None,
            recipient_list=[cd['to']])
            sent= True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
    