from django.contrib.auth.models import User
from django.test import TestCase
from blog.models import Category, Post


class CommentDataTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_superuser(
            username='admin', 
            email='admin@github.com', 
            password='admin')
        cate = Category.objects.create(name='test')
        self.post = Post.objects.create(
            title='test_title',
            content='test_content',
            category=cate,
            author=user,
        )