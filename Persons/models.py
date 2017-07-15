# from django.db import models
# from django.contrib.auth.models import User
# from django.utils.translation import ugettext as _
# from Charity.models import Institute, Location
# from django.db.models.fields.files import ImageField
#
#
# # Y = 'y'
# # N = 'n'
# # YES_OR_NO_CHOICES = (
# #     (Y, 'بله'),
# #     (N, 'خیر')
# # )
# #
# #
# # class Profile(models.Model):
# #     user = models.OneToOneField(User,
# #                                 on_delete=models.CASCADE,
# #                                 unique=True,
# #                                 verbose_name=_('user'),
# #                                 related_name='profile')
# #     M = 'm'  # man
# #     W = 'w'
# #     GENDER_CHOICES = (
# #         (M, 'آقا'),
# #         (W, 'خانم'),
# #     )
# #     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=M, verbose_name='جنسیت')
# #     age = models.IntegerField(verbose_name='سن')
# #     SH = 'sh'
# #     SO = 'so'
# #     CH = 'Ch'
# #     J = 'j'
# #     O = 'o'
# #     RELIGION_CHOICES = (
# #         (SH, 'اسلام-شیعه'),
# #         (SO, 'اسلام-اهل سنت'),
# #         (CH, 'مسیحی'),
# #         (J, 'یهودی'),
# #         (O, 'سایر'),
# #     )
# #     religion = models.CharField(max_length=3, choices=RELIGION_CHOICES, default=SH, verbose_name='دین-مذهب')
# #     national_code = models.CharField(max_length=10, default=None, verbose_name='کد ملی')
# #     profile_image = ImageField(blank=True, null=True, verbose_name='عکس')
# #     location = models.ForeignKey(Location, verbose_name='آدرس')
# #     is_married = models.CharField(choices=YES_OR_NO_CHOICES, max_length=1, default=N, verbose_name='متاهل است؟')
# #     address = models.CharField(max_length=72, default=None, verbose_name='آدرس', null=True, blank=True)
# #     phone_num = models.CharField(max_length=11, verbose_name='شماره تلفن همراه')  # num of num???
# #     # accounts ???????????
# #     # education ?????????????
# #     job = models.CharField(max_length=40, default=None, verbose_name='شغل')  # choice ? num of job ???????????
# #     voluntary_experience = models.CharField(choices=YES_OR_NO_CHOICES, max_length=1, default=N,
# #                                             verbose_name='تجربه کارهای داوطلبانه؟')  # explanation ? choice ???????????
# #     monthly_cooperation_time = models.IntegerField(verbose_name='حد اقل زمان همکاری در ماه')  # time or project ???????
# #     favorites = models.CharField(max_length=50, default=None,
# #                                  verbose_name='علاقه مندی ها')  # explanation ? choice ???????????
# #
# #
# # class Case(models.Model):
# #     first_name = models.CharField(max_length=30, verbose_name='نام')
# #     last_name = models.CharField(max_length=30, verbose_name='نام خانوادگی')
# #     father_name = models.CharField(max_length=30, verbose_name='نام پدر')
# #     national_code = models.CharField(max_length=10, unique=True, verbose_name='کد ملی')
# #     profile_image = ImageField(blank=True, null=True, verbose_name='عکس')
# #     MALE = 'male'
# #     WOMEN = 'women'
# #     gender_choices = (
# #         (MALE, 'آقا'),
# #         (WOMEN, 'خانم'),
# #     )
# #     gender = models.CharField(max_length=6, choices=gender_choices, default=MALE, verbose_name='جنسیت')
# #     phone_num = models.CharField(max_length=11, verbose_name='شماره تلفن همراه')
# #     address = models.CharField(max_length=250, null=True, blank=True, verbose_name='آدرس')  # is changeable
# #     institute = models.ForeignKey(Institute, verbose_name='موسسه حمایت کننده')  # is changeable
# #
# #     def __str__(self):
# #         return str(self.first_name) + " " + str(self.last_name)
# #
# #     # def get_registration_date(self):
# #     #     return Status_history.objects.filter(member=self).first().date
# #
# #     class Meta:
# #         verbose_name = 'مددجو'
# #         verbose_name_plural = 'مددجویان'
