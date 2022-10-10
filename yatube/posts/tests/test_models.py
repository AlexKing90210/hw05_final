from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from django.core.cache import cache

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostModelTest.user)

    def test_models_post_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post

        self.assertEqual(str(post), post.text[:15])

    def test_models_group_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group

        self.assertEqual(str(group), group.title)

    def test_post_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses_post = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }

        for field, expected_value in field_verboses_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_group_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        group = PostModelTest.group
        field_verboses_group = {
            'title': 'Заголовок',
            'slug': 'Слаг',
            'description': 'Описание группы',
        }

        for field, expected_value in field_verboses_group.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value)

    def test_post_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post

        field_help_texts_post = {
            'text': 'Введите текст поста',
            'pub_date': 'Введите дату публикации поста',
            'author': 'Выберите автора поста',
            'group': 'Группа, к которой будет относиться пост',
        }

        for field, expected_value in field_help_texts_post.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)

    def test_group_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        group = PostModelTest.group

        field_help_texts_group = {
            'title': 'Дайте краткое название группе',
            'slug': 'Укажите ключ адреса страницы группы',
            'description': 'Опишите группу',
        }

        for field, expected_value in field_help_texts_group.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text, expected_value)
