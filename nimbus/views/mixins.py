from django.core.exceptions import ImproperlyConfigured, PermissionDenied

from braces.views import AccessMixin, PermissionRquiredMixin

class CheckObjectOwnerMethodMixin(object):
    user_attribute = 'user'
    raise_exception = False

    def check_object_owner(self, request):
        is_owner = getattr(self.get_object(), self.user_attribute) == request.user

        if not is_owner:
            if self.raise_exception:
                raise PermissionDenied
            else:
                return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        else:
            return True

    def get_object():
        raise NotImplementedError

    def get_login_url():
        raise NotImplementedError

    def get_redirect_field_name():
        raise NotImplementedError

class CheckUserPermissionMethodMixin(object):
    permission_required = None
    raise_exception = False

    def check_user_permission(self, request):
        if self.permission_required is None:
            raise ImproperlyConfigured("'CheckUserPermissionMethodMixin' requires " "'permission_required' attribute to be set.")

        has_permission = request.user.has_perm(self.permission_required)

        if not has_permission:
            if self.raise_exception:
                raise PermissionDenied
            else:
                return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

        return super(PermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs)

    def get_login_url():
        raise NotImplementedError

    def get_redirect_field_name():
        raise NotImplementedError


class CheckObjectOwnerMixin(CheckObjectOwnerMethodMixin, AccessMixin):
    """
    View mixin which verifies that the logged in user is the owner of the object of the view.
    Should only be used with a CBV that subclasses SingleObjectMixin or one that otherwise
    provides a get_object() method.

    Class Settings
    `user_attribute` - the attribute on the object that defines the owner. Detaulfs to 'user'
    `login_url` - the login url of site
    `redirect_field_name` - defaults to "next"
    `raise_exception` - defaults to False - raise 403 if set to True

    Example Usage

    class SomeView(CheckObjectOwnerMixin, DetailView):
        ...

        # optional
        user_attribute = 'owner'
        login_url = "/signup/"
        redirect_field_name = "hollaback"
        raise_exception = True
        ...
    """

    def dispatch(self, request, *args, **kwargs):
        if self.check_object_owner(request):
            return super(CheckObjectOwnerMixin, self).dispatch(request, *args, **kwargs)

class CheckObjectOwnerOrUserPermissionMixin(CheckUserPermissionMethodMixin, AccessMixin):
    """
    View mixin which verifies that the logged in user is the owner of the object of the view
    or that the user has the permission needed to access the object.
    Should only be used with a CBV that subclasses SingleObjectMixin or one that otherwise
    provides a get_object() method.

    Class Settings
    `user_attribute` - the attribute on the object that defines the owner. Detaulfs to 'user'
    `login_url` - the login url of site
    `redirect_field_name` - defaults to "next"
    `raise_exception` - defaults to False - raise 403 if set to True

    Example Usage

    class SomeView(CheckObjectOwnerMixin, DetailView):
        ...

        # required
        permission_required = "app.permission"

        # optional
        user = 'owner'
        login_url = "/signup/"
        redirect_field_name = "hollaback"
        raise_exception = True
        ...
    """

    def dispatch(self, request, *args, **kwargs):
        try:
            self.check_object_owner(request)
        except PermissionDenied:
            if self.check_user_permission(request):
                return super(CCheckObjectOwnerOrUserPermissionMixin, self).dispatch(request, *args, **kwargs)