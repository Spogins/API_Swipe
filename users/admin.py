from django.contrib import admin

from users.models import User, Role, Messages, Subscription, UserSubscription, Notary, SavedFilters


admin.site.register(User)
admin.site.register(Role)
admin.site.register(Messages)
admin.site.register(Subscription)
admin.site.register(UserSubscription)
admin.site.register(Notary)
admin.site.register(SavedFilters)
