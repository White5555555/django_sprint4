"""
Модуль утилит для приложения 'blog'.

Содержит вспомогательные функции, которые используются в представлениях
(views) для выполнения общих задач, таких как пагинация и формирование
базовых запросов к базе данных для постов.
"""

# Импорт необходимых модулей и классов.
from django.core.paginator import Paginator  # Класс для реализации
# постраничного вывода.
from django.db.models import Count  # Агрегатная функция для подсчета
# связанных объектов.
from django.utils import timezone  # Модуль для работы с текущим временем.

# Импорт констант и моделей, используемых в утилитах.
from blog.constants import DEFAULT_NUM_PAGE, POSTS_ON_PAGE
from blog.models import Post


def posts_pagination(request, posts):
    """
    Обрабатывает пагинацию для списка постов.

    Принимает текущий HTTP-запрос и QuerySet (или список) постов,
    и возвращает объект страницы пагинатора.

    Args:
        request: Объект HTTP-запроса Django.
        posts: QuerySet или список объектов Post для пагинации.

    Returns:
        Объект страницы пагинатора (`django.core.paginator.Page`),
        представляющий текущую страницу с постами.
    """
    # Получаем номер текущей страницы из GET-параметров запроса.
    # Если параметр 'page' отсутствует, используется значение
    # по умолчанию DEFAULT_NUM_PAGE.
    page_number = request.GET.get(
        'page',
        DEFAULT_NUM_PAGE
    )
    # Создаем экземпляр пагинатора, указывая QuerySet постов и количество
    # постов на одной странице (из константы POSTS_ON_PAGE).
    paginator = Paginator(posts, POSTS_ON_PAGE)
    # Возвращаем объект страницы для указанного номера.
    return paginator.get_page(page_number)


def query_post(
        manager=Post.objects,
        filters=True,
        with_comments=True
):
    """
    Формирует базовый QuerySet для постов с возможностью настройки.

    Позволяет получить QuerySet постов с предзагруженными связанными
    объектами (author, location, category), фильтрацией по статусу
    и дате публикации, а также с аннотацией количества комментариев.
    """
    # Создаем базовый QuerySet, используя `select_related` для оптимизации
    # запросов к базе данных при доступе к ForeignKey полям
    # (`author`, `location`, `category`).
    # `select_related` выполняет JOIN'ы в SQL-запросе.
    queryset = manager.select_related('author', 'location', 'category')

    # Применяем стандартные фильтры, если `filters` установлено в True.
    if filters:
        queryset = queryset.filter(
            is_published=True,  # Пост должен быть опубликован.
            pub_date__lt=timezone.now(),  # Дата публикации должна быть в
            # прошлом (меньше текущего времени).
            category__is_published=True  # Категория поста также
            # должна быть опубликована.
        )

    # Аннотируем QuerySet количеством связанных комментариев,
    # если `with_comments` True.
    if with_comments:
        # `annotate(comment_count=Count('comments'))`
        # добавляет новое поле 'comment_count'
        # к каждому объекту в QuerySet, содержащее
        # количество связанных комментариев
        # (используя обратную связь `comments`
        # из модели `Post.Meta.default_related_name`).
        queryset = queryset.annotate(comment_count=Count('comments'))

    # Сортируем полученный QuerySet по дате публикации в убывающем порядке
    # (последние посты сначала).
    return queryset.order_by('-pub_date')
