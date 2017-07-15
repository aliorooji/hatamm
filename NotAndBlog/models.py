from django.db import models
from Charity.models import Institute, HelperProfile, Project
from django_jalali.db import models as jmodels
from django.db.models.fields.files import ImageField
import os
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


def get_image_blog(instance, file_name):
    filename = str(instance.id) + ".jpg"
    return os.path.join('static/photos',
                        "post",
                        filename)


# Create your models here.
class Notification(models.Model):
    objects = jmodels.jManager()
    helper = models.ForeignKey(HelperProfile, verbose_name='مددکار', related_name='notifications', default=None,
                               null=True,
                               blank=True)
    institute = models.ForeignKey(Institute, verbose_name='موسسه', related_name='notifications', default=None,
                                  null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name='پروژه', related_name='notifications', default=None, null=True,
                                blank=True)
    text = models.TextField(default=None, max_length=3000, verbose_name='متن پیام', null=True, blank=True)
    date = jmodels.jDateField(verbose_name='تاریخ', default=None, null=True, blank=True)
    subject = models.CharField(max_length=72, default=None, verbose_name='موضوع', null=True, blank=True)
    profile_image = ImageField(upload_to=get_image_blog, blank=True, null=True, verbose_name='عکس')
    P_I_P = 'p_i_p'
    P_HA = 'p_ha'
    P_HE = 'p_he'
    R_HA = 'r_ha'
    R_HE = 'r_he'
    R_I = 'r_i'
    N_HA_I = 'n_ha_i'
    N_HA_HE = 'n_ha_he'
    N_I_HA = 'n_i_ha'
    N_I_HE = 'n_i_he'
    N_HE_HA = 'n_he_ha'
    N_HE_I = 'n_he_i'
    N_TYPE_CHOICES = (
        (P_I_P, 'پست موسسه درباره پروژه'),
        (P_HA, ''),
        (P_HE, ''),
        (R_HA, ''),
        (R_HE, 'گزارش مددکار توسط موسسه'),
        (R_I, ''),
        (N_HA_I, ''),
        (N_HA_HE, ''),
        (N_I_HA, ''),
        (N_I_HE, ''),
        (N_HE_I, ''),
        (N_HE_HA, ''),
    )
    n_type = models.CharField(max_length=10, default=None, choices=N_TYPE_CHOICES, verbose_name='نوع')
    tag1 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag2 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')
    tag3 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag4 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag5 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')
    tag6 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def __str__(self):
        return self.n_type
