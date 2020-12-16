from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Category, Post


class PostModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            username="admin", email="admin@github.com", password="admin"
        )
        cate = Category.objects.create(name="test")
        self.post = Post.objects.create(
            title="test_title",
            content="test_content",
            category=cate,
            author=user,
        )

    def test_str_representation(self):
        self.assertEqual(self.post.__str__(), self.post.title)

    def test_auto_populate_modified_at(self):
        self.assertIsNotNone(self.post.modified_at)
        old_post_modified_at = self.post.modified_at
        self.post.content = "test_new_content"
        self.post.save()
        self.post.refresh_from_db()
        self.assertTrue(self.post.modified_at > old_post_modified_at)

    def test_auto_populate_abstract(self):
        self.assertIsNotNone(self.post.abstract)
        self.assertTrue(0 < len(self.post.abstract) <= 54)

    def test_increase_views(self):
        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)

        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 2)


if __name__ == "__main__":
    pass
