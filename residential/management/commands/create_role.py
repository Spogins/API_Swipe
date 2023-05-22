from django.core.management.base import BaseCommand

from users.models import Role


class Command(BaseCommand):
    ROLES = ['admin', 'manager', 'builder', 'user']

    def handle(self, *args, **options):
        if not Role.objects.all():
            for role in self.ROLES:
                Role.objects.create(role=role)
                print(f'{role} created')
            print('All role created')
