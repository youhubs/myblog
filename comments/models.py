from django.db import models


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '{}: {}'.format(self.name, self.text[:20])


if __name__ == "__main__":
    pass
