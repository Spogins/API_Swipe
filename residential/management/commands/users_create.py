from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand

from users.models import User, Role


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.all():
            role = Role.objects.get(role='admin')
            admin = User.objects.create(
                is_superuser=True,
                username='admin@admin.com',
                first_name='admin',
                last_name='admin',
                is_staff=True,
                phone=555555555,
                email='admin@admin.com',
                is_active=True,
                role=role
            )
            admin.set_password('swipe5231')
            admin.save()
            email = EmailAddress.objects.create(
                email=admin.email,
                verified=True,
                primary=True,
                user=admin
            )
            email.save()
            print('Amin created')
            role = Role.objects.get(role='manager')
            manager = User.objects.create(
                is_superuser=False,
                username='manager@manager.com',
                first_name='manager',
                last_name='manager',
                is_staff=True,
                phone=555555555,
                email='manager@manager.com',
                is_active=True,
                role=role
            )
            manager.set_password('swipe5231')
            manager.save()
            email = EmailAddress.objects.create(
                email=manager.email,
                verified=True,
                primary=True,
                user=manager
            )
            email.save()
            print('Manager created')
            role = Role.objects.get(role='builder')
            builder = User.objects.create(
                is_superuser=False,
                username='builder@builder.com',
                first_name='builder',
                last_name='builder',
                is_staff=False,
                phone=555555555,
                email='builder@builder.com',
                is_active=True,
                role=role
            )
            builder.set_password('swipe5231')
            builder.save()
            email = EmailAddress.objects.create(
                email=builder.email,
                verified=True,
                primary=True,
                user=builder
            )
            email.save()
            print('Builder created')
            role = Role.objects.get(role='user')
            user = User.objects.create(
                is_superuser=False,
                username='user@user.com',
                first_name='user',
                last_name='user',
                is_staff=False,
                phone=555555555,
                email='user@user.com',
                is_active=True,
                role=role
            )
            user.set_password('swipe5231')
            user.save()
            email = EmailAddress.objects.create(
                email=user.email,
                verified=True,
                primary=True,
                user=user
            )
            email.save()
            print('User created')
            print('All user created')
