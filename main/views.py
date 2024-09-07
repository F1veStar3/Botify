from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.conf import settings
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .forms import ProfileForm, ReviewForm, UserForm, NotificationForm
from .models import Events, MapPoint, Notification, RefundRequest, Stock, Transaction, Review
from .mixins import CommonContextMixin

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@user_passes_test(lambda u: u.is_superuser)
def send_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            users = User.objects.all()
            for user in users:
                Notification.objects.create(
                    user=user,
                    title=notification.title,
                    message=notification.message
                )
            return redirect('base')
    else:
        form = NotificationForm()

    return render(request, 'send_notification.html', {'form': form})


def get_common_context():
    mixin = CommonContextMixin()
    return mixin.get_common_context()


def base(request):
    events = Events.objects.order_by('-id')[:3]

    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()

    context = {
        'events': events,
        'form': form,
    }
    context.update(get_common_context())

    return render(request, 'index.html', context)


def about(request):
    reviews = Review.objects.order_by('-id')[:15]

    context = {
        'reviews': reviews,

    }
    context.update(get_common_context())

    return render(request, 'about.html', context)


@login_required
def profile_view(request):
    user = request.user
    mixin = CommonContextMixin()
    common_context = mixin.get_common_context()
    stock = common_context.get('stock')

    user_transactions = Transaction.objects.filter(user=user)
    total_quantity = user_transactions.aggregate(Sum('quantity'))['quantity__sum']
    total_price = user_transactions.aggregate(Sum('total_price'))['total_price__sum']

    transactions = user_transactions.order_by('-id')
    paginator = Paginator(transactions, 10)  # 5 коментарів на сторінку
    page_number = request.GET.get('page', 1)
    t_page_obj = paginator.get_page(page_number)

    notifications = Notification.objects.filter(user=user).order_by('-id')
    paginator = Paginator(notifications, 3)
    page_number = request.GET.get('page')
    n_page_obj = paginator.get_page(page_number)

    user_form = UserForm(instance=user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':

        if 'user_form' in request.POST:
            user_form = UserForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect('profile')
        elif 'pay_form' in request.POST:
            quantity = int(request.POST.get('quantity'))
            total_price = quantity * stock.price_per_unit

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(total_price * 100),

                        'product_data': {
                            'name': f'Количество: {quantity}',
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',

                metadata={
                    'quantity': quantity,
                    'total_price': total_price,
                    'user_id': request.user.id,
                }
            )

            return redirect(session.url, code=303)
        else:
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')

    context = {
        'stock': stock,
        'user_form': user_form,
        'profile_form': profile_form,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'user_transactions': user_transactions,

        't_page_obj': t_page_obj,
        'n_page_obj': n_page_obj,
    }

    if request.htmx:
        if 'trigger' in request.headers and request.headers['trigger'] == 'transactions':
            return render(request, 'partials/transactions_list.html', {'t_page_obj': t_page_obj})
        elif 'trigger' in request.headers and request.headers['trigger'] == 'notifications':
            return render(request, 'partials/notification_list.html', {'n_page_obj': n_page_obj})

    return render(request, 'profile.html', context)


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return render(request, 'payment_successful.html')


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return render(request, 'payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return JsonResponse({'status': 'invalid payload or signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Отримуємо метадані
        user_id = session['metadata']['user_id']
        quantity = session['metadata']['quantity']
        session_id = session.get('id')
        total_price = session['metadata']['total_price']

        user = User.objects.get(id=user_id)
        stock = Stock.objects.get(id=1)  # Отримуємо об'єкт складу за ID

        transaction = Transaction.objects.create(
            user=user,
            quantity=quantity,
            stock=stock,
            stripe_checkout_id=session_id,
            total_price=total_price
        )

        notification = Notification.objects.create(
            user=user,
            title="Оплата прошла успешно",
            message=f"Ваша оплата на сумму {total_price}$ была успешно завершена. Спасибо за покупку!"
        )

        stock.remaining_quantity -= int(quantity)
        stock.save()

    return JsonResponse({'status': 'success'}, status=200)


class MapPointsAPI(View):
    def get(self, request):
        points = MapPoint.objects.all().values('name', 'latitude', 'longitude')
        return JsonResponse(list(points), safe=False)


@require_POST
def process_refund(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    refund_request, created = RefundRequest.objects.get_or_create(
        user=request.user,
        transaction=transaction,
        request_date=timezone.now()
    )

    if created:
        Notification.objects.create(
            user=request.user,
            title="Запрос на возврат отправлен",
            message=f"Ваш запрос на возврат средств по транзакции #{transaction.id} был успешно отправлен. Мы рассмотрим его в ближайшее время."
        )

    return redirect('profile')


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)
