
"""
Модуль моделей для приложения 'blog'.

Определяет структуру данных для основных сущностей блога:
Category (категории), Location (местоположения), Post (публикации)
и Comment (комментарии).

Модели наследуются от PublishedBaseModel для единообразного управления
статусами публикации и датами создания.
"""

from django.contrib.auth import get_user_model  # Текущую активную модель
# пользователя.
from django.db import models  # Базовый модуль для работы с моделями Django.
from django.urls import reverse  # Функция для генерации URL по имени маршрута.
from django.utils.text import Truncator  # Класс для усечения текста.

# Импорт констант из файла constants.py для использования в определениях полей.
from blog.constants import MAX_LENGTH, MAX_TEXT, MAX_WORDS_LENGTH

# Получаем модель пользователя.
# В settings.py
# AUTH_USER_MODEL настроена на стандартную или кастомную модель.
User = get_user_model()


class PublishedBaseModel(models.Model):
    """
    Абстрактная базовая модель для сущностей, которые могут быть опубликованы.

    Включает поля для статуса публикации (`is_published`) и даты создания
    (`created_at`).
    Используется как родительская модель для других моделей, чтобы избежать
    дублирования кода.
    """
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        # Указывает, что эта модель является абстрактной.
        abstract = True


class Category(PublishedBaseModel):
    """
    Модель, представляющая категорию публикации.

    Каждая категория имеет заголовок, описание, уникальный slug для URL
    и может быть опубликована или скрыта.
    """
    title = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        verbose_name='Заголовок',
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        # Настройки отображения в админке и для моделей.
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    # Метод __str__ для строкового представления объекта Category.
    # Усекает заголовок до MAX_WORDS_LENGTH слов.
    def str(self):
        return Truncator(self.title).words(MAX_WORDS_LENGTH)


class Location(PublishedBaseModel):
    """
    Модель, представляющая местоположение.

    Каждое местоположение имеет название и может быть опубликовано или скрыто.
    """
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название места',
    )

    class Meta:
        # Настройки отображения в админке и для моделей.
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    # Метод __str__ для строкового представления объекта Location.
    # Усекает название до MAX_WORDS_LENGTH слов.
    def str(self):
        return Truncator(self.name).words(MAX_WORDS_LENGTH)


class Post(PublishedBaseModel):
    """
    Модель, представляющая публикацию (пост) в блоге.

    Включает заголовок, текст, дату публикации, автора, местоположение,
    категорию и опциональное изображение.
    """
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Заголовок',
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.',
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении автора,
        # удаляются и его посты.
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,  # При удалении местоположения, поле
        # location в посте становится NULL.
        null=True,  # Позволяет полю location принимать значение NULL.
        verbose_name='Местоположение',
        blank=True,  # Позволяет полю быть пустым в форме
        # (необязательное поле).
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # При удалении категории, поле category
        # В посте становится NULL.
        null=True,  # Позволяет полю category принимать значение NULL.
        verbose_name='Категория',
    )
    image = models.ImageField(
        upload_to='post_images',  # Директория для сохранения загруженных
        # изображений.
        blank=True,  # Позволяет полю быть пустым в форме
        # (необязательное поле).
        verbose_name='Изображение к публикации'
    )

    class Meta:
        # default_related_name определяет имя, используемое для обратной связи
        # от объекта User к связанным Post. Например, user.posts.all().
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    # Метод __str__ для строкового представления объекта Post.
    # Усекает заголовок до MAX_WORDS_LENGTH слов.
    def str(self):
        return Truncator(self.title).words(MAX_WORDS_LENGTH)

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для объекта Post.

        Используется для перенаправлений после сохранения или редактирования,
        а также для генерации ссылок в шаблонах.
        """
        # Генерирует URL, соответствующий маршруту с именем 'post_detail'
        # в приложении 'blog', подставляя первичный ключ (pk) текущего поста.
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})


class Comment(PublishedBaseModel):
    """
    Модель, представляющая комментарий к публикации.

    Содержит текст комментария, автора и ссылку на публикацию,
    к которой он относится.
    """
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении автора, удаляются и его
        # комментарии.
        verbose_name='Автор',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,  # При удалении поста, удаляются и его
        # комментарии.
        verbose_name='Комментарий',  # В админке поле будет отображаться как
        # "Комментарий"
    )

    class Meta:
        # default_related_name определяет имя для обратной связи от
        # Post к Comment.
        # Например, post.comments.all().
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарий'  # В единственном числе
        # отображается "Комментарий"
        ordering = ('created_at',)  # По умолчанию комментарии сортируются по
        # дате создания.

    # Метод __str__ для строкового представления объекта Comment.
    # Отображает автора, пост и начало текста комментария.
    def str(self):
        return (f'Комментарий автора {self.author}'
                f'к посту "{self.post}",'
                f'текст: {self.text[:MAX_TEXT]}')
