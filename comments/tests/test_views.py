from django.urls import reverse
 
from .base import CommentDataTestCase
from ..models import Comment
 
 
class CommentViewTestCase(CommentDataTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('comments:comment', kwargs={'post_pk': self.post.pk})
 
    def test_invalid_comment_data(self):
        invalid_data = {
            'email': 'invalid_email',
        }
        response = self.client.post(self.url, invalid_data)
        self.assertTemplateUsed(response, 'comments/preview.html')
        self.assertIn('post', response.context)
        self.assertIn('form', response.context)
        form = response.context['form']
        for field_name, errors in form.errors.items():
            for err in errors:
                self.assertContains(response, err)
        self.assertContains(response, 'Comments failed. Please try again!')
 
    def test_valid_comment_data(self):
        valid_data = {
            'name': 'reviewer',
            'email': 'reviewer@review.com',
            'text': 'comments',
        }
        response = self.client.post(self.url, valid_data, follow=True)
        self.assertContains(response, 'Comments completed!')
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.name, valid_data['name'])
        self.assertEqual(comment.text, valid_data['text'])