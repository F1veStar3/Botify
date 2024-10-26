from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class Events(models.Model):
    name = models.CharField(max_length=225, verbose_name='Name')
    description = models.TextField(max_length=2000, verbose_name='Description')
    img = models.ImageField(verbose_name='Image', help_text='Recommended resolution: 800x533',
                            upload_to="events_imgs/")
    date = models.DateTimeField(default=timezone.now, verbose_name='Date')
    tag = models.CharField(max_length=225, verbose_name='Tag')
    url = models.URLField(max_length=200, verbose_name='Link', blank=True, null=True)

    class Meta:
        verbose_name = 'Content: News'
        verbose_name_plural = 'Content: News'


class Service(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField(max_length=2000)
    svg_icon = models.TextField(help_text="Insert SVG code")
    url = models.URLField(max_length=200, verbose_name='Link', blank=True, null=True)

    class Meta:
        verbose_name = 'Content: Features'
        verbose_name_plural = 'Content: Features'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    logo = models.ImageField(upload_to='logos/', blank=True, verbose_name='Logo')

    balance = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name='Balance')
    total_spent = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name='Total Spent')

    def update_balance_and_spent(self):
        transactions = Transaction.objects.filter(user=self.user)
        self.balance = transactions.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        self.total_spent = transactions.aggregate(total_price=Sum('total_price'))['total_price'] or 0
        self.save()

    def get_logo(self):
        if self.logo:
            return self.logo.url
        return '/media/logos/user.png'

    class Meta:
        verbose_name = 'Monitoring: Profile'
        verbose_name_plural = 'Monitoring: Profiles'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Stock(models.Model):
    id = models.AutoField(primary_key=True, default=1)
    price_per_unit = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Price per unit')
    total_quantity = models.PositiveIntegerField(verbose_name='Total quantity')
    minimum_purchase_quantity = models.PositiveIntegerField(verbose_name='Minimum purchase quantity')

    remaining_quantity = models.PositiveIntegerField(verbose_name='Remaining quantity')

    class Meta:
        verbose_name = 'Payment: Stock'
        verbose_name_plural = 'Payment: Stocks'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='Stock')
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total price')
    stripe_checkout_id = models.CharField(max_length=500, verbose_name='stripe_id', null=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Date and time')

    class Meta:
        verbose_name = 'Payment: Transaction'
        verbose_name_plural = 'Payment: Transactions'


@receiver(post_delete, sender=Transaction)
def update_stock_on_transaction_delete(sender, instance, **kwargs):
    stock = instance.stock
    total_quantity = stock.total_quantity or 0
    sum_quantity = Transaction.objects.filter(stock=stock).aggregate(
        models.Sum('quantity'))['quantity__sum'] or 0
    stock.remaining_quantity = total_quantity - sum_quantity
    stock.save()


@receiver(post_save, sender=Transaction)
def update_stock_on_transaction_save(sender, instance, **kwargs):
    stock = instance.stock
    total_quantity = stock.total_quantity or 0
    sum_quantity = Transaction.objects.filter(stock=stock).aggregate(
        models.Sum('quantity'))['quantity__sum'] or 0
    stock.remaining_quantity = total_quantity - sum_quantity
    stock.save()


@receiver(post_save, sender=Transaction)
@receiver(post_delete, sender=Transaction)
def update_profile_on_transaction_change(sender, instance, **kwargs):
    profile = Profile.objects.get(user=instance.user)
    profile.update_balance_and_spent()


class RefundRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, verbose_name='Transaction')
    request_date = models.DateTimeField(default=timezone.now, verbose_name='Request date')

    class Meta:
        verbose_name = 'Communication: Refund Request'
        verbose_name_plural = 'Communication: Refund Requests'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='User')
    title = models.CharField(max_length=225, verbose_name='Title')
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')

    class Meta:
        verbose_name = 'Communication: Notification'
        verbose_name_plural = 'Communication: Notifications'


class Massage(models.Model):
    name = models.CharField(max_length=225, verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=225, verbose_name='Subject')
    message = models.TextField(verbose_name='Message', max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')

    class Meta:
        verbose_name = 'Communication: Questions'
        verbose_name_plural = 'Communication: Questions'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    subject = models.CharField(max_length=225, verbose_name='Subject')
    message = models.TextField(verbose_name='Message', max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')

    class Meta:
        verbose_name = 'Communication: Review'
        verbose_name_plural = 'Communication: Reviews'

