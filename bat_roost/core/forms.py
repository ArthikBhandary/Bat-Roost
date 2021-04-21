from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class AdminAuthForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        print("Here")
        if not user.is_admin:
            raise ValidationError(
                _("This is not an admin account"),
                code="non_admin",
            )

        return super(AdminAuthForm, self).confirm_login_allowed(user)
