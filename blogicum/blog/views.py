from django.shortcuts import (
    get_object_or_404,
    render
)
from django.utils import timezone

from blog.models import Category, Post


def get_posts(posts=Post.objects):
    """Посты из БД."""
    return posts.select_related(
        'category',
        'location',
        'author',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    """Главная страница."""
    return render(request, 'blog/index.html', {
        'posts': get_posts()[:5],
    })


def post_detail(request, post_id):
    """Полное описание выбранной записи."""
    return render(request, 'blog/detail.html', {
        'post': get_object_or_404(get_posts(), pk=post_id),
    })


def category_posts(request, category_slug):
    """Публикация категории."""
    # Получение объекта запрашиваемой категории.
    category = get_object_or_404(
        Category,
        slug=category_slug
    )

    return render(request, 'blog/category.html', {
        'category': category,
        # Получение всех постов category.
        'post_list': get_posts(category.posts),
    })
