from django.contrib import admin

from residential.models import Complex, Section, Corps, Floor, Flat, Documents, ChessBoard

# Register your models here.
admin.site.register(Complex)
admin.site.register(Section)
admin.site.register(Corps)
admin.site.register(Floor)
admin.site.register(Flat)
admin.site.register(Documents)
admin.site.register(ChessBoard)