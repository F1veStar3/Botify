from django.shortcuts import get_object_or_404
from .models import Transaction, User, Stock, Service


class CommonContextMixin:
    def get_common_context(self):
        transaction_count = Transaction.objects.count()
        user_count = User.objects.count()
        services = Service.objects.all()
        stock = get_object_or_404(Stock, id=1)

        invested = stock.total_quantity - stock.remaining_quantity

        return {
            'invested':invested,
            'transaction_count': transaction_count,
            'user_count': user_count,
            'stock': stock,
            'services': services,
        }
