
from .models import Message

def user_notifications(request):
    if request.user.is_authenticated:
        messages = Message.objects.filter(recipient=request.user).order_by('-created_at')[:5]
        return {'user_messages': messages}
    return {'user_messages': []}