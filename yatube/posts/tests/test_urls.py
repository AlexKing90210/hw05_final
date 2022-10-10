from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, Client

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testUser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
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
        self.authorized_client.force_login(PostURLTests.user)

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            "/": "posts/index.html",
            f"/group/{self.group.slug}/": "posts/group_list.html",
            f"/profile/{self.user.username}/": "posts/profile.html",
            f"/posts/{self.post.id}/": "posts/post_detail.html",
            f"/posts/{self.post.id}/edit/": "posts/post_create.html",
            "/create/": "posts/post_create.html",
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(template)
                self.assertTemplateUsed(response, url)

    # Проверяем общедоступные страницы
    # def test_home_url_exists_at_desired_location(self):
    #    """Страница / доступна любому пользователю."""
    #    response = self.guest_client.get('/')
    #    self.assertEqual(response.status_code, HTTPStatus.OK)

    # def test_group_slug_url_exists_at_desired_location(self):
    #    """Страница /group/slug/ доступна любому пользователю."""
    #    response = self.guest_client.get('/group/test-slug/')
    #    self.assertEqual(response.status_code, HTTPStatus.OK)

    # def test_profile_username_url_exists_at_desired_location(self):
    #    """Страница /profile/username/ доступна любому пользователю."""
    #    response = self.guest_client.get('/profile/testUser/')
    #    self.assertEqual(response.status_code, HTTPStatus.OK)

    # def test_posts_postid_url_exists_at_desired_location(self):
    #    """Страница /posts/post_id/ доступна любому пользователю."""
    #    response = self.guest_client.get(f'/posts/{self.post.id}/')
    #    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_exists_at_desired_location(self):
        templates_url_names = {
            "/": "posts/index.html",
            f"/group/{self.group.slug}/": "posts/group_list.html",
            f"/profile/{self.user.username}/": "posts/profile.html",
            f"/posts/{self.post.id}/": "posts/post_detail.html",
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(template)
                self.assertTemplateUsed(response, url)

    def test_unexisting_page_url_exists_at_desired_location(self):
        """Страница unexisting_page доступна любому пользователю."""
        response = self.guest_client.get('/unexisting_page/')
        # Проверьте, что статус ответа сервера - 404
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        # Проверьте, что используется шаблон core/404.html
        self.assertTemplateUsed(response, 'core/404.html')
        
    # Проверяем доступность страниц для авторизованного пользователя
    def test_posts_create_exists_at_desired_location(self):
        """Страница /posts/create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Проверяем доступность страницы редактирования поста только его автору
    def test_posts_edit_exists_at_desired_location(self):
        """Страница /posts/edit/ доступна только автору."""
        self.user = User.objects.get(username=self.user)
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)
        response = self.authorized_client.get(f"/posts/{self.post.id}/edit/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
    