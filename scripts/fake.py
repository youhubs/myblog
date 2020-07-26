import os
import pathlib
import random
import sys
from datetime import timedelta

import django
from django.utils import timezone

import faker

# add project path
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == "__main__":
    # start django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")
    django.setup()

    from blog.models import Category, Post, Tag
    from comments.models import Comment
    from django.contrib.auth.models import User

    print("clean database")
    Post.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Comment.objects.all().delete()
    User.objects.all().delete()

    print("create a blog user")
    user = User.objects.create_superuser(
        "admin", "admin@github.com", "admin")

    category_list = ["Note Book", "Open Source", "Java Tips", "Python Tips"]
    tag_list = [
        "django",
        "Python",
        "Pipenv",
        "Docker",
        "Nginx",
        "Elasticsearch",
        "Gunicorn",
        "Supervisor",
        "test tag",
    ]
    a_year_ago = timezone.now() - timedelta(days=365)

    print("create categories and tags")
    for cate in category_list:
        Category.objects.create(name=cate)

    for tag in tag_list:
        Tag.objects.create(name=tag)

    print("create a markdown sample post")
    Post.objects.create(
        title="Markdown and font highlight",
        content=pathlib.Path(BASE_DIR)
        .joinpath("scripts", "md.sample")
        .read_text(encoding="utf-8"),
        category=Category.objects.create(name="Markdown"),
        author=user,
    )

    print("create some faked posts published within the past year")
    fake = faker.Faker()  # English
    for _ in range(100):
        tags = Tag.objects.order_by("?")
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by("?").first()
        created_at = fake.date_time_between(
            start_date="-1y", end_date="now", tzinfo=timezone.get_current_timezone()
        )
        post = Post.objects.create(
            title=fake.sentence().rstrip("."),
            content="\n\n".join(fake.paragraphs(10)),
            created_at=created_at,
            category=cate,
            author=user,
        )
        post.tags.add(tag1, tag2)
        post.save()

    # fake = faker.Faker("zh_CN")
    # for _ in range(100):  # Chinese
    #     tags = Tag.objects.order_by("?")
    #     tag1 = tags.first()
    #     tag2 = tags.last()
    #     cate = Category.objects.order_by("?").first()
    #     created_at = fake.date_time_between(
    #         start_date="-1y", end_date="now", tzinfo=timezone.get_current_timezone()
    #     )
    #     post = Post.objects.create(
    #         title=fake.sentence().rstrip("."),
    #         content="\n\n".join(fake.paragraphs(10)),
    #         created_at=created_at,
    #         category=cate,
    #         author=user,
    #     )
    #     post.tags.add(tag1, tag2)
    #     post.save()

    print("create some comments")
    for post in Post.objects.all()[:20]:
        post_created_at = post.created_at
        delta_in_days = "-" + \
            str((timezone.now() - post_created_at).days) + "d"
        for _ in range(random.randrange(3, 15)):
            Comment.objects.create(
                name=fake.name(),
                email=fake.email(),
                url=fake.uri(),
                text=fake.paragraph(),
                created_at=fake.date_time_between(
                    start_date=delta_in_days,
                    end_date="now",
                    tzinfo=timezone.get_current_timezone(),
                ),
                post=post,
            )

    print("done!")
