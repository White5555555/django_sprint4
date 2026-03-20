"""
Модуль маршрутов (URL-адресов) для приложения 'blog'.

Определяет, какие URL-адреса будут обрабатываться views
из модуля `views.py` приложения. Использует `path` для создания
URL-шаблонов и `include` для группировки связанных маршрутов.

`app_name` устанавливает пространство имен для этих URL-маршрутов,
чтобы избежать конфликтов с маршрутами из других приложений Django.
"""

# Импорт необходимых функций для работы с URL.
from django.urls import include, path

# Импорт всех представлений (views) из приложения 'blog'.
from blog import views

# Установка пространства имен для URL-маршрутов этого приложения.
# Это позволяет использовать префикс 'blog:' при обращении к URL
# (например, в шаблонах или при перенаправлениях).
app_name = 'blog'

# Определение списка маршрутов, связанных с постами.
posts = [
    # Маршрут для отображения детальной информации о конкретном посте.
    # <int:post_id> - переменная часть URL, принимающая целое число (ID поста).
    path('<int:post_id>/', views.post_detail, name='post_detail'),

    # Маршрут для создания нового поста.
    path('create/', views.create_post, name='create_post'),

    # Маршрут для редактирования существующего поста.
    # <int:post_id> - ID поста, который нужно редактировать.
    path('<int:post_id>/edit/', views.edit_post, name='edit_post'),

    # Маршрут для удаления существующего поста.
    # <int:post_id> - ID поста, который нужно удалить.
    path('<int:post_id>/delete/', views.delete_post, name='delete_post'),

    # Маршрут для добавления комментария к посту.
    # <int:post_id> - ID поста, к которому добавляется комментарий.
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),

    # Маршрут для редактирования существующего комментария.
    # <int:post_id> - ID поста, к которому относится комментарий.
    # <int:comment_id> - ID редактируемого комментария.
    path('<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),

    # Маршрут для удаления существующего комментария.
    # <int:post_id> - ID поста, к которому относится комментарий.
    # <int:comment_id> - ID удаляемого комментария.
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
]

# Определение списка маршрутов, связанных с профилем пользователя.
profile = [
    # Маршрут для редактирования профиля текущего пользователя.
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    # Маршрут для отображения профиля другого пользователя.
    # <str:username> - переменная часть URL, принимающая строку
    # (имя пользователя).
    path('<str:username>/', views.profile, name='profile'),
]

# Основной список URL-маршрутов для приложения 'blog'.
urlpatterns = [
    # Маршрут для главной страницы блога.
    # Пустая строка '' соответствует корневому URL приложения
    # (например, /blog/).
    path('', views.index, name='index'),

    # Маршрут для отображения постов конкретной категории.
    # <slug:category_slug> - переменная часть URL, принимающая slug категории
    # (например, /blog/category/tech/).
    path('category/<slug:category_slug>/',
         views.category_posts,
         name='category_posts'),

    # Включение списка маршрутов для постов под префиксом 'posts/'.
    # Например, /blog/posts/create/ будет вести к views.create_post.
    path('posts/', include(posts)),

    # Включение списка маршрутов для профилей под префиксом 'profile/'.
    # Например, /blog/profile/john_doe/ будет вести к views.profile.
    # 'edit_profile/' внутри этого include
    # будет доступен по адресу /blog/profile/edit_profile/.
    path('profile/', include(profile)),
]
