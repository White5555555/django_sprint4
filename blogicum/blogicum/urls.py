"""
Корневой модуль URL-маршрутов проекта 'blogicum'.

Этот файл определяет основные URL-шаблоны приложения, включая:
- Маршруты для административной панели Django.
- Маршруты для аутентификации пользователей (вход, выход, регистрация).
- Маршруты для статических страниц (например, 'about').
- Маршруты для основного приложения 'blog'.
- Интеграцию с debug_toolbar (в режиме отладки).

Также задает обработчики ошибок 404 и 500.
"""

# Импорт необходимых модулей и классов Django.
from django.conf.urls.static import static  # Для обслуживания медиафайлов
# в режиме DEBUG.
from django.contrib import admin  # Модуль для администрирования Django.
# `UserCreationForm` - стандартная форма Django для регистрации пользователей.
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy  # Функции для
# работы с URL.
# `CreateView` - универсальное представление для создания нового объекта.
from django.views.generic.edit import CreateView

# Импорт настроек проекта.
from blogicum import settings

# Обработчики ошибок.
# Устанавливаем пользовательские обработчики для страниц 404 (Не найдено)
# и 500 (Внутренняя ошибка сервера).
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

# Основной список URL-маршрутов проекта.
urlpatterns = [
    # Маршрут для статических страниц (например, "about", "contact").
    # Все URL-адреса, начинающиеся с 'pages/', будут обрабатываться
    # маршрутами из приложения 'pages'. `namespace='pages'` используется
    # для обращения к этим URL-адресам (например, `pages:about`).
    path('pages/', include('pages.urls', namespace='pages')),

    # Маршруты для аутентификации: вход, выход, сброс пароля и т.д.
    # Django предоставляет готовый набор URL-шаблонов для аутентификации.
    path('auth/', include('django.contrib.auth.urls')),

    # Маршрут для регистрации новых пользователей.
    # Используется `CreateView` для отображения формы регистрации.
    # `template_name` указывает на шаблон, `form_class` - на форму.
    # `success_url` - URL, на который пользователь будет перенаправлен после
    # успешной регистрации. `reverse_lazy` используется, чтобы избежать
    # цикла импортов, так как `blog:index` может еще не быть определен
    # на момент загрузки `urls.py`.
    path('auth/registration/', CreateView.as_view(
        template_name='registration/registration_form.html',
        form_class=UserCreationForm,
        success_url=reverse_lazy('blog:index')  # Перенаправление на
        # главную блога.
    ),
        name='registration'),  # Имя маршрута для регистрации.

    # Маршрут для административной панели Django.
    path('admin/', admin.site.urls),

    # Маршруты для основного приложения 'blog'.
    # Все URL-адреса, начинающиеся с корневого URL (''), будут обрабатываться
    # маршрутами из приложения 'blog'. `namespace='blog'` позволяет
    # обращаться к URL-адресам блога (например, `blog:post_detail`).
    path('', include('blog.urls', namespace='blog')),
]


# Условное добавление URL-маршрутов для debug_toolbar
# и обслуживания медиафайлов.
if settings.DEBUG:
    # Добавляем URL-маршруты для debug_toolbar,
    # если он установлен и DEBUG=True.
    # Это позволяет использовать инструменты отладки.
    urlpatterns += [
        path("debug/", include("debug_toolbar.urls")),
    ]
    # Добавляем маршруты для обслуживания медиафайлов
    # (изображений, документов).
    # `static()` создает URL-шаблоны, которые будут обслуживать файлы из
    # директории `settings.MEDIA_ROOT` по URL-пути `settings.MEDIA_URL`.
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
