from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Events, MapPoint, Transaction, Stock, Review, RefundRequest, Notification, Service, Massage, Profile


# Register your models here.
@admin.register(Events)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'tag', 'date']


@admin.register(Service)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(MapPoint)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Profile)
class PageAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'total_spent']


@admin.register(Transaction)
class PageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quantity', 'total_price', 'timestamp']


@admin.register(Stock)
class PageAdmin(admin.ModelAdmin):
    list_display = ['id', 'price_per_unit', 'total_quantity', 'minimum_purchase_quantity', 'remaining_quantity']


@admin.register(Review)
class PageAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'created_at']


@admin.register(Massage)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'created_at']


@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_id', 'request_date']

    def transaction_id(self, obj):
        return obj.transaction.id

    transaction_id.short_description = 'ID Транзакции'


@admin.register(Notification)
class PageAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'send_notification_link']

    def send_notification_link(self, obj):
        url = reverse('send_notification')
        return format_html('<a href="{}">Рассылка</a>', url)
