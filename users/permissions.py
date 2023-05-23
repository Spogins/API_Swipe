from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated, BasePermission

from announcements.models import *
from files.models import Photo
from residential.models import *
from users.models import SavedFilters


class CustomIsAuthenticated(IsAuthenticated):
    message = _('You do not have permission.')

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class IsBuilderPermission(BasePermission):
    message = _('You do not have permission.')

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.role == 'builder'


class IsAdminPermission(BasePermission):
    message = _('You do not have permission.')

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.role == 'admin'

    def has_object_permission(self, request, view, obj):
        return True


class IsManagerPermission(BasePermission):
    message = _('You do not have permission.')

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.role == 'manager'

    def has_object_permission(self, request, view, obj):
        return True


class IsOwnerPermission(BasePermission):
    message = _('You do not have permission.')

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Complex):
            return request.user == obj.user
        elif isinstance(obj, (Flat, Section, Floor, Corps, Documents, ChessBoard)):
            return request.user == obj.residential_complex.user
        elif isinstance(obj, (SavedFilters, Favorites)):
            return request.user == obj.user

        return False


class IsCreatorPermission(BasePermission):
    message = _('You do not have permission.')

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Flat):
            return request.user == obj.user
        return False


class IsUserPermission(BasePermission):
    message = _('You do not have permission.')

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.role == 'user'


class IsResidentialComplexOrFlatPhotoOwner(BasePermission):
    message = _('You do not have permission.')

    def has_object_permission(self, request, view, obj: Photo):
        try:
            return request.user == obj.gallery.residentialcomplex.owner
        except ObjectDoesNotExist:
            pass

        try:
            return request.user == obj.gallery.flat.residential_complex.owner
        except ObjectDoesNotExist:
            return False


class IsChessBoardFlatPhotoOwner(BasePermission):
    message = _('You do not have permission.')

    def has_object_permission(self, request, view, obj: Photo):
        return request.user == obj.gallery.chessboardflat.creator \
            or request.user == obj.gallery.chessboardflat.residential_complex.user