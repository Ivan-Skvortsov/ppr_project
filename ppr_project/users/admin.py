from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import User, Group

from users.tasks import send_email_task


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
    list_display = ('username', 'first_name', 'last_name', 'email',
                    'is_active')
    actions = ['make_user_active']

    @admin.action(
        description='Сделать пользователей активными и оповестить их по email'
    )
    def make_user_active(self, request, queryset):
        for user in queryset:
            user.is_active = True
            subject = 'Аккаунт одобрен администратором!'
            message = (f'Привет, {user.get_full_name()}! Отличные новости: '
                       'твой аккаунт в системе управления ППР КС-45 одобрен! '
                       'Можешь заходить, используя свой логин и пароль.\n'
                       'На всякий случай (если ты забыл), твой логин - '
                       f'{user.get_username()}\nСпасибо, что ты с нами!')
            user.save()
            send_email_task.delay(subject, message, [user.email])
        self.message_user(
            request, 'Пользователи оповещены!', messages.SUCCESS
            )
