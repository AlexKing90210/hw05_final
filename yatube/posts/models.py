from django.db.models.constraints import Q
from django.db import models
from django.contrib.auth import get_user_model

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        help_text='Дайте краткое название группе')
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text='Укажите ключ адреса страницы группы')
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Опишите группу')

    class Meta:
        verbose_name_plural = 'Группы'
    
    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        help_text='Введите дату публикации поста',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Выберите автора поста',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    # Поле для картинки (необязательное)
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='posts/',
        help_text='Аватар профиля',
        blank=True
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        related_name='comments',
        blank=True,
        null=True,
        verbose_name='Комментарии к посту',
        help_text='Комментарии поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        help_text='Автор комментария к посту',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(CreatedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], 
                name='unique follows'
                ),
            # models.CheckConstraint(
            #    check=Q(user__gt=author),
            #    name='Dont subscribe to yourself'
            # )
        ]

    # Ограничить подписку на себя и дублирующие подписки
