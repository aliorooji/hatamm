from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Notification
# import datetime
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from Charity import jalali
import jdatetime


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["text", "profile_image"]
