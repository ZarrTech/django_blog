from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse

# custom model manager
class PublishedManager(models.Manager):
 def get_queryset(self):
    return (
    super().get_queryset().filter(status=Post.Status.PUBLISHED
    ))

# Create your models here.
class Post(models.Model):
    #status Post model class
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'published'
    #Post info variable model
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date=
'published')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT,
    )
    objects= models.Manager()
    published_manager = PublishedManager()
    class meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published']),
        ]
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args= [self.published.year, self.published.month, self.published.day, self.slug]
        )