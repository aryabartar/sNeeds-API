from django.shortcuts import render, get_object_or_404
from .models import Post, Booklet, Topic


# Create your views here.
def home(request):
    def shorter_strings(post):
        return post.text[0:140]

    def get_post_images_urls(post):
        return post.post_image.url

    posts_size = int(len(Post.objects.all()))
    booklet_size = int(len(Booklet.objects.all()))
    first_three_posts_bodies = Post.objects.all().reverse()[posts_size-3:posts_size]
    first_three_posts_bodies = list(map(shorter_strings, first_three_posts_bodies))
    first_three_posts_images = list(map(get_post_images_urls, Post.objects.all().reverse()[posts_size-3:posts_size]))

    my_dict = {"first_three_posts" : Post.objects.all().reverse()[posts_size-3:posts_size],
               "first_three_posts_bodies": first_three_posts_bodies,
               "first_three_posts_images": first_three_posts_images,
               "first_three_booklets" : Booklet.objects.all()[booklet_size-3:booklet_size]}

    return render(request, 'website/home.html', context=my_dict)

def get_post (request , pk) :
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'website/post.html' , context={"post" :post})

def get_booklet (request , pk) :
    booklet = get_object_or_404(Booklet, pk=pk)
    return render(request, 'website/booklet.html' , context={"booklet" :booklet})

def get_categories (request , slug) :
    category = get_object_or_404(Topic , slug=slug)
    return render(request , 'website/category.html' , context={})