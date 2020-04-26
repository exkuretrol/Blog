from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post

class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='password'
        )
        self.post = Post.objects.create(
            title='Helloworld',
            body='Body',
            author=self.user
        )
    
    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/posts/1/')

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'Helloworld')
        self.assertEqual(f'{self.post.body}', 'Body')
        self.assertEqual(f'{self.post.author}', 'testuser')
    
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Body')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_post_detailed_view(self):
        response = self.client.get('/posts/1/')
        no_response = self.client.get('/posts/200000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Helloworld')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New text',
            'author': self.user,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')

    def test_post_edit_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Update title',
            'body': 'Update body,'
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)
