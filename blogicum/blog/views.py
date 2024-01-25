from datetime import datetime

from django.shortcuts import get_object_or_404, render

from .const_num import POSTS_COUNT
from .models import Category, Post


def posts():
    """Получение информации из БД."""
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )


def index(request):
    """Главная страница."""
    return render(request, 'blog/index.html',
                  {'post_list': posts()[:POSTS_COUNT]})


def post_detail(request, post_id):
    """Отображение полного описания записи."""
    post = get_object_or_404(posts(), id=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Отображение публикаций категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    context = {'category': category,
               'post_list': posts().filter(category=category)}
    return render(request, 'blog/category.html', context)
