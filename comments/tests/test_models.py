from .base import CommentDataTestCase
from ..models import Comment


class CommentModelTestCase(CommentDataTestCase):

    def setUp(self):
        super().setUp()
        self.comment = Comment.objects.create(
            name='reviewer',
            email='reviewer@review.com',
            text='comments',
            post=self.post,
        )

    def test_str_representation(self):
        self.assertEqual(self.comment.__str__(), 'reviewer: comments')