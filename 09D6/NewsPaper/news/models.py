from django.db import models
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm

class Author(models.Model):
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id_user.username}'

    def update_rating(self):
        author_articles = Post.objects.filter(id_author=self, post_type=Post.article)

        # суммарный рейтинг каждой статьи автора умножается на 3
        post_list = author_articles.values("post_rating")
        if not post_list:
            rating = 3 * (sum(item["post_rating"] for item in post_list))
        else:
            rating = 0

        # суммарный рейтинг всех комментариев автора
        comment_rating_list = Comment.objects.filter(id_user=self.id_user).values("comment_rating")
        rating += sum(item["comment_rating"] for item in comment_rating_list)

        # суммарный рейтинг всех комментариев к статьям автора
        for posts in author_articles:
            comment_in_post = Comment.objects.filter(id_post=posts).values("comment_rating")
            rating += sum(item["comment_rating"] for item in comment_in_post)

        self.author_rating = rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscriber = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    article = 'A'
    news = 'N'
    POSTING_TYPE = [(article, 'статья'), (news, 'новость')]

    id_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=1, choices=POSTING_TYPE, default=article)
    post_created = models.DateTimeField(auto_now_add=True)
    id_post_category = models.ManyToManyField(Category, through="PostCategory")
    post_header = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        result = self.post_text[:124] + '...'
        return result

    def __str__(self):
        return f'{self.post_header.title()}('+self.post_text[:12]+'); Рейтиг = '+str(self.post_rating)

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

class PostCategory(models.Model):
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_created = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


