from django.urls import path
from .views import base, info_for_investors, MapPointsAPI, profile_view, process_refund, custom_404, payment_successful, \
    payment_cancelled, stripe_webhook, send_notification

handler404 = custom_404

urlpatterns = [
    path('', base, name='base'),
    path('info_for_investors/', info_for_investors, name='info_for_investors'),
    path('api/points/', MapPointsAPI.as_view(), name='map_points_api'),
    path('profile/', profile_view, name='profile'),
    path('refund/<int:transaction_id>/', process_refund, name='process_refund'),
    path('payment_successful/', payment_successful, name='payment_successful'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),
    path('webhook/stripe/', stripe_webhook, name='stripe_webhook'),
    path('send-notification/', send_notification, name='send_notification'),
]
