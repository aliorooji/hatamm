from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from jalali_date import admin as jalalidate_admin
from .models import Notification
from jet.filters import RelatedFieldAjaxListFilter


class NotificationAdmin(jalalidate_admin.ModelAdmin):
    list_display = ('id', 'helper', 'institute', 'project', 'date', 'n_type')
    list_filter = (
        ('date', DateFieldListFilter),
        'n_type',
        ('institute', RelatedFieldAjaxListFilter),
        ('helper', RelatedFieldAjaxListFilter),
        ('project', RelatedFieldAjaxListFilter),
    )
    list_per_page = 40

# --------------------------=======end main classes======------------------------------
admin.site.register(Notification, NotificationAdmin)
