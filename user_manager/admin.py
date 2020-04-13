from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from django.conf.urls import url
from django.contrib.auth.models import User
from django.urls import path, reverse
from django.utils.html import format_html

from user_manager.tasks import send_email_to_user

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_list_template = "admin/custom_change_list.html"

    list_display = (
        'id',
        'username',
        'email',
        'user_actions',
    )

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()

        custom_urls = [
            path('send_emails', self.send_emails),
            path('send_emails/<int:pk>', self.notify_user, name="notify"),
        ]
        return custom_urls + urls

    def notify_user(self, request, **kwargs):
        user_id = kwargs.get('pk')
        send_email_to_user.delay(user_id)
        return HttpResponseRedirect("../")

    def send_emails(self, request):
        for obj in self.model.objects.all():
            send_email_to_user.delay(obj.id)
        return HttpResponseRedirect("../")

    def user_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Send Notification</a>',
            reverse('admin:notify', args=[obj.pk]),
        )

    user_actions.short_description = 'User Actions'
    user_actions.allow_tags = True
