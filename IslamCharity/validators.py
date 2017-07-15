from django import forms
import re
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

@deconstructible
class CustomUsernameValidator(object):
    message = _('Invalid username')

    def __call__(self, value):
        if not re.match(r'[a-zA-Z0-9_@#-]+', value):
            raise forms.ValidationError(_('لطفا کاراکتر های بدون فاصله وارد کنید.'))

custom_username_validators = [CustomUsernameValidator]
