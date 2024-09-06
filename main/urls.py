from django.urls import path
from .views import base, about, MapPointsAPI, profile_view, process_refund, custom_404, payment_successful, \
    payment_cancelled

handler404 = custom_404

urlpatterns = [
    path('', base, name='base'),
    path('about/', about, name='about'),
    path('api/points/', MapPointsAPI.as_view(), name='map_points_api'),
    path('profile/', profile_view, name='profile'),
    path('refund/<int:transaction_id>/', process_refund, name='process_refund'),

    path('payment_successful/', payment_successful, name='payment_successful'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),
    # path('stripe_webhook', stripe_webhook, name='stripe_webhook'),
]
