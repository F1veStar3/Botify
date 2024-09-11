from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class Events(models.Model):
    name = models.CharField(max_length=225, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    img = models.ImageField(verbose_name='Изображение', help_text='Рекомендованное разрешение: 800x533',
                            upload_to="events_imgs/")
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    tag = models.CharField(max_length=225, verbose_name='Тег')
    url = models.URLField(max_length=200, verbose_name='Ссылка', blank=True, null=True)  # Нове поле для посилання

    class Meta:
        verbose_name = 'Контент: Новости'
        verbose_name_plural = 'Контент: Новости'


class Service(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField(max_length=2000)
    svg_icon = models.TextField(help_text="Вставте SVG код")

    class Meta:
        verbose_name = 'Контент: Возможности'
        verbose_name_plural = 'Контент: Возможности'


class MapPoint(models.Model):
    name = models.CharField(max_length=225, verbose_name='Название')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')

    class Meta:
        verbose_name = 'Контент: Точка на карте'
        verbose_name_plural = 'Контент: Точки на карте'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    logo = models.ImageField(upload_to='logos/', blank=True, verbose_name='Логотип')

    balance = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name='Баланс')
    total_spent = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name='На общую сумму')

    def update_balance_and_spent(self):
        transactions = Transaction.objects.filter(user=self.user)
        self.balance = transactions.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        self.total_spent = transactions.aggregate(total_price=Sum('total_price'))['total_price'] or 0
        self.save()

    def get_logo(self):
        if self.logo:
            return self.logo.url
        return '/media/logos/anonim.png'

    class Meta:
        verbose_name = 'Мониторинг: Профиль'
        verbose_name_plural = 'Мониторинг: Профили'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Stock(models.Model):
    id = models.AutoField(primary_key=True, default=1)
    price_per_unit = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Цена за единицу')
    total_quantity = models.PositiveIntegerField(verbose_name='Общее количество')
    minimum_purchase_quantity = models.PositiveIntegerField(verbose_name='Минимальное количество для покупки')

    remaining_quantity = models.PositiveIntegerField(verbose_name='Оставшееся количество')

    class Meta:
        verbose_name = 'Оплата: Акция'
        verbose_name_plural = 'Оплата: Акции'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='Акция')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Итоговая цена')
    stripe_checkout_id = models.CharField(max_length=500, verbose_name='stripe_id', null=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')

    class Meta:
        verbose_name = 'Оплата: Транзакция'
        verbose_name_plural = 'Оплата: Транзакции'


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, verbose_name='Транзакция')
    request_date = models.DateTimeField(default=timezone.now, verbose_name='Дата запроса')

    class Meta:
        verbose_name = 'Коммуникация: Запрос на возврат'
        verbose_name_plural = 'Коммуникация:  Запросы на возврат'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='Пользователь')
    title = models.CharField(max_length=225, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Коммуникация: Уведомление'
        verbose_name_plural = ' Коммуникация: Уведомления'


class Massage(models.Model):
    name = models.CharField(max_length=225, verbose_name='Имя')
    email = models.EmailField(verbose_name='Электронная почта')
    subject = models.CharField(max_length=225, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение', max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Коммуникация: Вопросы'
        verbose_name_plural = 'Коммуникация: Вопросы'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    subject = models.CharField(max_length=225, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение', max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Коммуникация: Отзыв'
        verbose_name_plural = 'Коммуникация: Отзывы'
