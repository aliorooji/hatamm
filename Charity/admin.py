from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from jalali_date import admin as jalalidate_admin
from .models import HelperProfile, Project, ManyToMany, HelpType, Case, Institute
# from jet.filters import
from jet.filters import RelatedFieldAjaxListFilter
# from jet.filters import DateRangeFilter
from jet.admin import CompactInline


def accept_these(ModelAdmin, request, queryset):
    queryset.update(accepted=True)


def not_accepted_these(ModelAdmin, request, queryset):
    queryset.update(accepted=False)


accept_these.short_description = "تایید شون کن"
not_accepted_these.short_description = "تایید نشده شون کن"

#
# class CaseAdmin(jalalidate_admin.ModelAdmin):
#     list_display = ['id', 'national_code']


class HelperProfileAdmin(jalalidate_admin.ModelAdmin):
    list_display = ['id', 'user']
    list_filter = (
        ('user__date_joined', DateFieldListFilter),
        ('user__last_login', DateFieldListFilter),
        ('user', RelatedFieldAjaxListFilter),
    )
    list_per_page = 40


class ProjectAdmin(jalalidate_admin.ModelAdmin):
    list_display = ('id', 'title', 'institute', 'help_type', 'start_date', 'end_date', 'accepted')
    list_filter = (
        ('start_date', DateFieldListFilter),
        ('end_date', DateFieldListFilter),
        'accepted',
        ('institute', RelatedFieldAjaxListFilter),
    )
    actions = [accept_these, not_accepted_these]
    list_per_page = 40


class InstituteAdmin(jalalidate_admin.ModelAdmin):
    list_display = ['id', 'title', 'accepted', 'establishment_date']
    list_filter = (
        'accepted',
    )
    actions = [accept_these, not_accepted_these]
    list_per_page = 40


class MtmAdmin(jalalidate_admin.ModelAdmin):
    list_display = ['id', 'project', 'helper', 'institute', 'status', 'the_date']
    list_filter = (
        'status',
        ('project', RelatedFieldAjaxListFilter),
        ('institute', RelatedFieldAjaxListFilter),
        ('helper', RelatedFieldAjaxListFilter),
        ('the_date', DateFieldListFilter),
    )
    list_per_page = 40


class HelpTypeAdmin(jalalidate_admin.ModelAdmin):
    list_display = ['id', 'title', 'father']
    list_per_page = 100


# --------------------------=======end main classes======------------------------------
# admin.site.register(Case, CaseAdmin)
admin.site.register(HelperProfile, HelperProfileAdmin)
admin.site.register(HelpType, HelpTypeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Institute, InstituteAdmin)
admin.site.register(ManyToMany, MtmAdmin)
