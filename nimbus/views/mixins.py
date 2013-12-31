from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth.views import redirect_to_login

from braces.views import AccessMixin, PermissionRequiredMixin
from actstream import action

class CheckObjectOwnerMethodMixin(object):
    user_attribute = 'user'

    def check_object_owner(self, request):
        is_owner = getattr(self.get_object(), self.user_attribute) == request.user

        if not is_owner:
            return False
        else:
            return True

class CheckUserPermissionMethodMixin(object):
    permission_required = None

    def check_user_permission(self, request):
        if self.permission_required is None:
            raise ImproperlyConfigured("'CheckUserPermissionMethodMixin' requires " "'permission_required' attribute to be set.")

        has_permission = request.user.has_perm(self.permission_required)

        if not has_permission:
            return False
        else:
            return True

class CheckAccessMixin(AccessMixin):
    def check_access(self, request, *args, **kwargs):
        raise NotImplementedError

    def redirect_to(self, *args, **kwargs):
        return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def dispatch(self, request, *args, **kwargs):
        if self.check_access(request, *args, **kwargs):
            return super(CheckAccessMixin, self).dispatch(request, *args, **kwargs)
        elif self.raise_exception:
            raise PermissionDenied
        else:
            return self.redirect_to()

class CheckObjectOwnerMixin(CheckObjectOwnerMethodMixin, CheckAccessMixin):
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

    def check_access(self, request, *args, **kwargs):
        return self.check_object_owner(request)

class CheckObjectOwnerOrUserPermissionMixin(CheckObjectOwnerMethodMixin, CheckUserPermissionMethodMixin, CheckAccessMixin):
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

    def check_access(self, request, *args, **kwargs):
        if self.check_object_owner(request):
            return True
        elif self.check_user_permission(request):
            return True
        else:
            return False

class GenerateActionMixin(object):
    actor = None
    verb = None
    action_object = None
    target = None

    def generate_action(self, actor=None, verb=None, action_object=None, target=None, *args, **kwargs):
        if not actor:
            actor = self.get_action_actor()
        if not verb:
            verb = self.get_action_verb()
        if not action_object:
            action_object = self.get_action_action_object()
        if not target:
            target = self.get_action_target()

        if not actor:
            raise ValueError(("Generating an action requires 'actor' to be defined, "
                "either as an argument on the generate_action method call, as an "
                "attribute on the class or by overriding the get_action_actor method "
                "on the class."))
        if not verb:
            raise ValueError(("Generating an action requires 'verb' to be defined, "
                "either as an argument on the generate_action method call, as an "
                "attribute on the class or by overriding the get_action_verb method "
                "on the class."))

        action.send(actor, verb=verb, action_object=action_object, target=target)

    def get_action_actor(self, *args, **kwargs):
        return self.actor

    def get_action_verb(self, *args, **kwargs):
        return self.verb

    def get_action_action_object(self, *args, **kwargs):
        return self.action_object

    def get_action_target(self, *args, **kwargs):
        return self.target