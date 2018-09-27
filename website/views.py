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
    first_three_posts_bodies = Post.objects.all().reverse()[posts_size - 3:posts_size]
    first_three_posts_bodies = list(map(shorter_strings, first_three_posts_bodies))
    first_three_posts_images = list(map(get_post_images_urls, Post.objects.all().reverse()[posts_size - 3:posts_size]))

    my_dict = {"first_three_posts": Post.objects.all().reverse()[posts_size - 3:posts_size],
               "first_three_posts_bodies": first_three_posts_bodies,
               "first_three_posts_images": first_three_posts_images,
               "first_three_booklets": Booklet.objects.all()[booklet_size - 3:booklet_size]}

    return render(request, 'website/home.html', context=my_dict)


def get_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    breadcrumbs_link = post.get_cat_list()
    category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
    breadcrumbs = zip(breadcrumbs_link, category_name)
    print("---")
    print(list(breadcrumbs))
    return render(request, "website/post.html", {'post': post, 'breadcrumbs': breadcrumbs})


def get_booklet(request, pk):
    booklet = get_object_or_404(Booklet, pk=pk)
    return render(request, 'website/booklet.html', context={"booklet": booklet})


def show_category(request, hierarchy=None):
    category_slug = hierarchy.split('/')
    category_queryset = list(Topic.objects.all())
    all_slugs = [x.slug for x in category_queryset]
    parent = None
    for slug in category_slug:
        if slug in all_slugs:
            parent = get_object_or_404(Topic, slug=slug, parent=parent)
    return render(request, "website/category.html",
                  {'post_set': parent.posts.all(), 'sub_categories': parent.children.all()})


def blog_posts(request, page=1):
    '''
    This method is used to show different blog posts in one page .
    :param request: 
    :return: 
    '''
    post_per_page = 1  # If you want to change number of posts in a blog page,change this.
    blog_pages_number = int(len(Post.objects.all()))  # for determining all blog pages size

    def first_10_words(text):
        splitted_text = text.split(" ")
        temp_text = ""
        counter = 0
        for word in splitted_text:
            temp_text += str(word + " ")
            counter += 1
            if counter > 10:
                temp_text += " ... "
                break
        return temp_text

    def get_first_words_of_post(posts):
        text_list = []
        for post in posts:
            text_list.append(first_10_words(post.text))
        return text_list

    def get_blog_page_numbers(page):
        page_number_list = []
        if page - 2 > 0:
            page_number_list.append((page - 2, True))
        if page - 1 > 0:
            page_number_list.append((page - 1, True))
        page_number_list.append((page, False))
        if page < blog_pages_number:
            page_number_list.append((page + 1, True))
        if page + 1 < blog_pages_number:
            page_number_list.append((page + 2, True))
        return page_number_list

    all_posts = Post.objects.all()[(page - 1) * post_per_page:page * post_per_page]
    descriptions_text = get_first_words_of_post(all_posts)
    post_list = list(zip(all_posts, descriptions_text))  # The first one is post and second is description
    my_dict = {"post_list": post_list, "page_number": get_blog_page_numbers(page)}
    return render(request, "website/blog-posts.html", context=my_dict)
