from .models import Post, Comment
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        # labels = {
        #     'text': ('Текст поста'),
        #     'group': ('Группа'),
        #     'image': ('Аватар профиля')
        # }
        # help_texts = {
        #     'text': ('Введите текст поста'),
        #     'group': ('Укажите группу для поста'),
        #     'image': ('Загрузите аватар для пользователя')
        # }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        # labels = {
        #    'text': ('Текст комментария')
        # }
        # help_texts = {
        #    'text': ('Введите текст комментария')
        # }
