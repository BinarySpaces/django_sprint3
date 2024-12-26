from django.utils import timezone
from django.shortcuts import (
    get_list_or_404,
    get_object_or_404,
    render
)

from blog.models import Post, Category


current_time = timezone.now()


def get_posts():
    """Посты из БД."""
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    )


def index(request):
    """Главная страница."""
    post_list = get_posts().order_by("-pub_date")[:5]
    context = {'post_list': post_list}

    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    """Полное описание выбранной записи."""
    post = get_object_or_404(get_posts(), pk=id)
    context = {'post': post}

    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Публикация категории."""
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    post_list = get_list_or_404(
        get_posts().filter(category__slug=category_slug)
    )
    context = {'category': category, 'post_list': post_list}

    return render(request, 'blog/category.html', context)
