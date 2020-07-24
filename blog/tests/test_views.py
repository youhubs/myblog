from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import Category, Tag, Post


class BlogDataTestCase(TestCase):

    def setUp(self):
        # User
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@github.com',
            password='admin'
        )
 
        # Category
        self.cate1 = Category.objects.create(name='category_1')
        self.cate2 = Category.objects.create(name='category_2')
 
        # Tag
        self.tag1 = Tag.objects.create(name='tag_1')
        self.tag2 = Tag.objects.create(name='tag_2')
 
        # Post
        self.post1 = Post.objects.create(
            title='title_1',
            content='content_1',
            category=self.cate1,
            author=self.user,
        )
        self.post1.tags.add(self.tag1)
        self.post1.save()
 
        self.post2 = Post.objects.create(
            title='title_2',
            content='content_2',
            category=self.cate2,
            author=self.user,
        )


class CategoryViewTestCase(BlogDataTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('posts:category', kwargs={'pk': self.cate1.pk})
        self.url2 = reverse('posts:category', kwargs={'pk': self.cate2.pk})

    def test_visit_a_nonexistent_category(self):
        url = reverse('posts:category', kwargs={'pk': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_without_any_post(self):
        Post.objects.all().delete()
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(response, 'No Posts!')

    def test_with_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(response, self.post1.title)
        self.assertIn('posts', response.context)
        self.assertIn('is_paginated', response.context)
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['posts'].count(), 1)
        expected_qs = self.cate1.post_set.all().order_by('-created_at')
        self.assertQuerysetEqual(response.context['posts'], [repr(p) for p in expected_qs])


class PostDetailViewTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.md_post = Post.objects.create(
            title='Markdown',
            content='markdown posts',
            category=self.cate1,
            author=self.user,
        )
        self.url = reverse('posts:detail', kwargs={'pk': self.md_post.pk})
 
    def test_good_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/detail.html')
        self.assertContains(response, self.md_post.title)
        self.assertIn('post', response.context)
 
    def test_visit_a_nonexistent_post(self):
        url = reverse('posts:detail', kwargs={'pk': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
 
    def test_increase_views(self):
        self.client.get(self.url)
        self.md_post.refresh_from_db()
        self.assertEqual(self.md_post.views, 1)
 
        self.client.get(self.url)
        self.md_post.refresh_from_db()
        self.assertEqual(self.md_post.views, 2)
 
    def test_markdownify_post_body_and_set_toc(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'title')
        self.assertContains(response, self.md_post.title)
 
        post_template_var = response.context['post']
        self.assertHTMLEqual(post_template_var.body_html, "<h1 id='title'>title</h1>")
        self.assertHTMLEqual(post_template_var.toc, '<li><a href="#title">title</li>')


if __name__ == "__main__":
    pass
