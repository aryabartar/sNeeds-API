from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Post, Booklet, Topic, BookletTopic, BookletField, UserUploadedBooklet
from .forms import UploadBooklet


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


def get_booklet(request, slug):
    booklet = get_object_or_404(Booklet, slug=slug.lower())
    booklet.number_of_views += 1  # increments view
    booklet.save()
    is_visited = request.session.get('is_visited', False)
    request.session['is_visited'] = True
    context = {"booklet": booklet, "is_visited": is_visited}
    return render(request, 'website/booklet.html', context=context)


class BookletTopicView(generic.ListView):
    model = BookletTopic
    template_name = 'website/booklet-topic.html'
    paginate_by = 4

    def get_queryset(self):
        qs = self.model.objects.all()
        if self.kwargs.get('slug'):
            booklet_topic = \
                qs.filter(
                    slug__exact=self.kwargs['slug'].lower(),
                    field__slug__exact=self.kwargs['field_slug'].lower()
                )[0]
            associated_booklets = booklet_topic.booklets.all().order_by('title')
        return associated_booklets


class BookletFieldView(generic.ListView):
    model = BookletField
    template_name = 'website/booklet-field.html'
    paginate_by = 4

    def get_queryset(self):
        qs = self.model.objects.all()
        if self.kwargs.get('slug'):
            qs = qs.filter(slug__exact=self.kwargs['slug'].lower())
            associated_topics = []
            for topic in qs[0].topics.all():
                associated_topics.append(topic)
        return associated_topics


def booklet_home(request):
    context = {"fields": BookletField.objects.all()}
    return render(request, "website/booklet-home.html", context=context)


def upload_booklet(request):
    if request.method == 'POST':
        upload_booklet_form = UploadBooklet(request.POST, request.FILES)
        if upload_booklet_form.is_valid():
            user_uploaded_booklet = UserUploadedBooklet(title=upload_booklet_form.cleaned_data['title'],
                                                        field=upload_booklet_form.cleaned_data['field'],
                                                        topic=upload_booklet_form.cleaned_data['topic'],
                                                        writer=upload_booklet_form.cleaned_data['writer'],
                                                        booklet_file=upload_booklet_form.cleaned_data['booklet_file'],
                                                        )
            user_uploaded_booklet.save()
            context = {'form': UploadBooklet(), 'success': True}
            return render(request, 'website/booklet-upload-by-user.html', context=context)

    else:
        upload_booklet_form = UploadBooklet()

    context = {'form': upload_booklet_form, 'success': False}
    return render(request, 'website/booklet-upload-by-user.html', context=context)


def booklet_search(request):
    print(request.GET.get('q'))
    return render(request, "website/search_results.html")
