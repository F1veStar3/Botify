from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Review)
admin.site.register(Events)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(MapPoint)
admin.site.register(Profile)
admin.site.register(Partner)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'subject', 'created_at', 'read')
    fields = ('recipient', 'subject', 'body', 'read')
    readonly_fields = ('created_at',)