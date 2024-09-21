
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'actor', 'verb', 'target', 'timestamp', 'read')
    list_filter = ('read', 'timestamp', 'verb')
    search_fields = ('recipient__username', 'actor__username', 'verb')