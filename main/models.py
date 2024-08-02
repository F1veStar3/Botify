from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Category(models.Model):
    name = models.CharField(max_length=225)
    tag = models.CharField(max_length=225, null=True)
    img = models.ImageField(verbose_name='800x600', upload_to="cat_imgs/")
    slug = models.SlugField(unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Menu(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # slug = models.SlugField()
    is_available = models.BooleanField(default=True)
    img = models.ImageField(verbose_name='800x600', upload_to="product_imgs/")

    def __str__(self):
        return self.name


class Review(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Events(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField(max_length=2000)
    img = models.ImageField(verbose_name='800x533', upload_to="events_imgs/")
    date = models.DateTimeField(default=timezone.now)
    tag = models.name = models.CharField(max_length=225)

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField(max_length=2000)
    img = models.ImageField(verbose_name='100x100', upload_to="partner_imgs/")

    def __str__(self):
        return self.name


class MapPoint(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    # first_name = models.CharField(max_length=30, blank=True)
    # last_name = models.CharField(max_length=30, blank=True)

    def get_logo(self):
        if self.logo:
            return self.logo.url
        return '/media/logos/anonim.png'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Message(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
