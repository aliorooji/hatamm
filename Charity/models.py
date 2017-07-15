from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
import os
from django_jalali.db import models as jmodels
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


def get_image_path(instance, file_name):
    filename = str(instance.id) + ".jpg"
    return os.path.join('static/photos', 'institute', filename)


def get_image_help_type(instance, file_name):
    filename = str(instance.id) + ".jpg"
    return os.path.join('static/photos', 'help_type', filename)


def get_image__i_or_p(instance, file_name):
    filename = str(instance.id) + ".jpg"
    return os.path.join('static/photos', 'i_or_p', filename)


def get_image_name(instance, file_name):
    filename = str(instance.id) + ".jpg"
    return os.path.join('static/photos', 'helper', filename)


class HelperProfile(models.Model):
    objects = jmodels.jManager()
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile', null=True, blank=True)
    M = 'm'
    W = 'w'
    GENDER_CHOICES = (
        (M, 'آقا'),
        (W, 'خانم'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=M, verbose_name='جنسیت', null=True,
                              blank=True)
    birth_day = jmodels.jDateField(verbose_name='تاریخ تولد', default=None, null=True, blank=True)
    SH = 'sh'
    SO = 'so'
    CH = 'Ch'
    J = 'j'
    O = 'o'
    RELIGION_CHOICES = (
        (SH, 'اسلام-شیعه'),
        (SO, 'اسلام-اهل سنت'),
        (CH, 'مسیحی'),
        (J, 'یهودی'),
        (O, 'سایر'),
    )
    religion = models.CharField(max_length=3, choices=RELIGION_CHOICES, default=SH, verbose_name='دین-مذهب', null=True,
                                blank=True)
    about_you = models.TextField(null=True, max_length=2000, blank=True, default=None, verbose_name='درباره شما')
    national_code = models.CharField(max_length=10, default=None, verbose_name='کد ملی', unique=True,
                                     )
    profile_image = ProcessedImageField(upload_to=get_image_name, blank=True, null=True, verbose_name='عکس',
                                        processors=[ResizeToFill(200, 200)],
                                        format='JPEG',
                                        options={'quality': 100})
    lat = models.FloatField(verbose_name='lat', default=None, null=True, blank=True)
    lng = models.FloatField(verbose_name='lng', default=None, null=True, blank=True)
    is_married = models.BooleanField(default=False, verbose_name='متاهل؟', blank=True)
    address = models.CharField(max_length=72, default=None, verbose_name='آدرس', null=True, blank=True)
    phone_num = models.CharField(max_length=11, verbose_name='شماره تلفن همراه', default=None)
    job = models.CharField(max_length=40, default=None, verbose_name='شغل', null=True,
                           blank=True)
    monthly_cooperation_time = models.IntegerField(verbose_name='حد اقل زمان همکاری در ماه', null=True, blank=True)
    twitter = models.CharField(max_length=72, default=None, verbose_name='توییتر شما', null=True,
                               blank=True)
    telegram = models.CharField(max_length=72, default=None, verbose_name='تلگرام شما', null=True,
                                blank=True)
    facebook = models.CharField(max_length=72, default=None, verbose_name='فیس بوک شما', null=True,
                                blank=True)
    instagram = models.CharField(max_length=72, default=None, verbose_name='اینستاگرام شما', null=True,
                                 blank=True)
    others_view_u = models.BooleanField(blank=True, default=True, verbose_name='دیگران شما را ببینند؟')
    in_home_page = models.BooleanField(blank=True, default=False, verbose_name='')
    tag1 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag4 = models.BooleanField(blank=True, default=False, verbose_name='')
    city = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='شهر')
    province = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='استان')
    tag5 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')
    tag6 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')

    class Meta:
        verbose_name = 'پروفایل مددکار'
        verbose_name_plural = ' پروفایل مددکاران'

    def __str__(self):
        return self.user.username

    @staticmethod
    def autocomplete_search_fields():
        return 'user__username',


class HelpType(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان', default=None)
    father = models.ForeignKey('self', null=True, blank=True, verbose_name='ریشه', related_name='children',
                               default=None)
    image = models.ImageField(upload_to=get_image_help_type, default=None, null=True, blank=True)
    SH = 'sh'
    SO = 'so'
    CH = 'Ch'
    J = 'j'
    O = 'o'
    TYPE_CHOICES = (
        (SH, ''),
        (SO, ''),
        (CH, ''),
        (J, ''),
        (O, ''),
    )
    type_type = models.CharField(max_length=3, choices=TYPE_CHOICES, default=SH, verbose_name='نوع', null=True,
                                 blank=True)
    tag1 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag2 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag3 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')
    tag4 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')

    class Meta:
        verbose_name = 'انواع پروژه'
        verbose_name_plural = 'انواع پروژه ها'

    def __str__(self):
        m_father = None
        f_list = [self]
        for h_t in f_list:
            if h_t.father:
                if h_t.father.father:
                    f_list.append(h_t.father)
                else:
                    m_father = h_t.father
        if m_father:
            return m_father.title + ' ' + '»' + ' ' + self.title
        else:
            return self.title

    @staticmethod
    def autocomplete_search_fields():
        return 'title',


class Institute(models.Model):
    objects = jmodels.jManager()
    title = models.CharField(max_length=100, default=None, verbose_name='عنوان')  #
    admin = models.ForeignKey(User, null=True, blank=True, verbose_name='ادمین', default=None, related_name='institute')
    lat = models.FloatField(verbose_name='lat', default=None, null=True, blank=True)
    lng = models.FloatField(verbose_name='lng', default=None, null=True, blank=True)
    help_type1 = models.ForeignKey(HelpType, verbose_name='نوع کمک رسانی', related_name='institute1', default=None,
                                   null=True, blank=True)
    help_type2 = models.ForeignKey(HelpType, verbose_name='نوع کمک رسانی', related_name='institute2', default=None,
                                   null=True, blank=True)
    help_type3 = models.ForeignKey(HelpType, verbose_name='نوع کمک رسانی', related_name='institute3', default=None,
                                   null=True, blank=True)
    patent_num = models.CharField(max_length=10, verbose_name='شماره ثبت', default=None, null=True, blank=True)  #
    profile_image = ProcessedImageField(upload_to=get_image_path, verbose_name='عکس',
                                        help_text='این عکس میتواند عکس موسسه یا هر چیز دیگری باشد.',
                                        processors=[ResizeToFill(600, 420)],
                                        format='JPEG',
                                        options={'quality': 100})
    address = models.CharField(max_length=200, verbose_name='آدرس', default=None, null=True, blank=True)  #
    establishment_date = jmodels.jDateField(verbose_name='تاریخ تاسیس', default=None, null=True, blank=True)  #
    site_address = models.CharField(max_length=64, verbose_name='آدرس سایت', null=True, blank=True, default=None)  #
    phone_num = models.CharField(max_length=11, verbose_name='شماره تلفن',
                                 default=None)
    phone_num2 = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره تلفن',
                                  default=None)
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل', default=None)
    post_code = models.CharField(max_length=10, verbose_name='کد پستی',
                                 default=None, null=True, blank=True)  #
    explanation = models.TextField(verbose_name='توضیحات', max_length=6000, default=None, null=True, blank=True,
                                   help_text='شامل تاریخچه و اهداف')
    twitter = models.CharField(max_length=72, default=None, verbose_name='توییتر موسسه', null=True,
                               blank=True)  #
    telegram = models.CharField(max_length=72, default=None, verbose_name='تلگرام موسسه', null=True,
                                blank=True)  #
    facebook = models.CharField(max_length=72, default=None, verbose_name='فیس بوک موسسه', null=True,
                                blank=True)  #
    instagram = models.CharField(max_length=72, default=None, verbose_name='اینستاگرام موسسه', null=True,
                                 blank=True)  #
    agent = models.CharField(max_length=72, default=None, help_text='این شخص رابط بین حاتم و موسسه مربوط میباشد.',
                             verbose_name='نام و نام خانوادگی نماینده')  #
    agent_job = models.CharField(max_length=72, default=None, help_text='این شخص رابط بین حاتم و موسسه مربوط میباشد.',
                                 verbose_name='جایگاه نمانده در موسسه')  #
    agent_num = models.CharField(max_length=11, default=None, help_text='این شخص رابط بین حاتم و موسسه مربوط میباشد.',
                                 verbose_name='شماره همراه نماینده')  #
    accepted = models.BooleanField(blank=True, default=False, verbose_name='تایید شده')
    in_home_page = models.BooleanField(blank=True, default=False, verbose_name='در صفحه ی اول باشد')
    tag1 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag6 = models.BooleanField(blank=True, default=False, verbose_name='')
    n_score = models.IntegerField(null=True, blank=True, default=None, verbose_name='امتیاز منفی')
    city = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='شهر')
    province = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='استان')
    tag5 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')

    class Meta:
        verbose_name = 'موسسه'
        verbose_name_plural = 'موسسات'

    def __str__(self):
        return self.title

    @staticmethod
    def autocomplete_search_fields():
        return 'title',


class Case(models.Model):
    objects = jmodels.jManager()
    national_code = models.CharField(max_length=10, unique=True, verbose_name='کد ملی', default=None)
    M = 'm'
    W = 'w'
    GENDER_CHOICES = (
        (M, 'آقا'),
        (W, 'خانم'),
    )
    is_married = models.BooleanField(default=False, verbose_name='متاهل؟', blank=True)
    tag8 = jmodels.jDateField(verbose_name='تاریخ تولد', default=None, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default=M, verbose_name='جنسیت', null=True,
                              blank=True)
    job = models.CharField(max_length=40, default=None, verbose_name='شغل', null=True,
                           blank=True)
    explanation = models.TextField(verbose_name='توضیحات', max_length=3000, default=None, null=True, blank=True)
    institute = models.ForeignKey(Institute, verbose_name='موسسه حمایت کننده', default=None,
                                  related_name='cases', null=True, blank=True)
    tag1 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag3 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag4 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag2 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')
    tag5 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')
    tag6 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')

    def __str__(self):
        return str(self.national_code)

    class Meta:
        verbose_name = 'مددجو'
        verbose_name_plural = 'مددجویان'


class Project(models.Model):
    objects = jmodels.jManager()
    title = models.CharField(max_length=100, default=None, verbose_name='عنوان')
    sentence = models.CharField(max_length=200, default=None, verbose_name='پروژه در جمله')
    institute = models.ForeignKey(Institute, verbose_name='موسسه تعریف کننده', related_name='projects', default=None,
                                  null=True, blank=True)
    help_type = models.ForeignKey(HelpType, verbose_name='نوع کمک رسانی', related_name='projects', default=None)
    start_date = jmodels.jDateField(verbose_name='تاریخ شروع', default=None, null=True, blank=True)
    end_date = jmodels.jDateField(verbose_name='تاریخ پایان', default=None, null=True, blank=True)
    image = ProcessedImageField(upload_to=get_image_path, verbose_name='عکس', null=True, blank=True, default=None,
                                help_text='',
                                processors=[ResizeToFill(600, 420)],
                                format='JPEG',
                                options={'quality': 100})
    lat = models.FloatField(verbose_name='lat', default=None, null=True, blank=True)
    lng = models.FloatField(verbose_name='lng', default=None, null=True, blank=True)
    O = 'o'
    W_CH = 'w_ch'
    W_D = 'w_d'
    S_CH = 's_ch'
    E = 'e'
    AN = 'an'
    ADDRESSED_CHOICES = (
        (O, 'سایر'),
        (W_CH, 'کودکان کار'),
        (W_D, 'زنان بی سرپرست'),
        (S_CH, 'کودکان بیمار'),
        (E, 'محیط زیست'),
        (AN, 'حیوانات'),
    )
    addressed = models.CharField(max_length=10, choices=ADDRESSED_CHOICES, default=None,
                                 help_text='مخاطب پروژه شامل قشر و گروهی از مردم است که پروژه قرار است به آنها کمک کند',
                                 verbose_name='مخاطب پروژه')
    min_age = models.IntegerField(null=True, blank=True, default=None,
                                  verbose_name='کمترین سن ممکن برای خیر خواه')
    max_age = models.IntegerField(default=None, null=True, blank=True,
                                  verbose_name='بیشترین سن ممکن برای خیر خواه')
    gender = models.CharField(max_length=1, choices=HelperProfile.GENDER_CHOICES, default=None, verbose_name='جنسیت',
                              null=True,
                              blank=True)
    n_t_experience = models.BooleanField(default=False, verbose_name='نیاز به تجربه قبلی؟', blank=True)
    P = 'p'
    I = 'i'
    C = 'c'
    S = 's'
    FP = 'fp'
    FI = 'fi'
    IPT = 'ipt'
    STATUS_CHOICES = (
        (P, 'ممکن'),
        (I, 'ناممکن'),
        (C, 'قطعی'),
        (S, 'موفق'),
        (FP, 'فوری ممکن'),
        (FI, 'فوری ناممکن'),
        (IPT, 'مهم'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=None, verbose_name='وضعیت', null=True,
                              blank=True)
    case = models.ForeignKey(Case, verbose_name='مددجو', default=None, null=True, blank=True)
    from_home = models.BooleanField(default=False, verbose_name='از خانه؟', blank=True)
    accommodation = models.BooleanField(default=False, verbose_name='محل اقامت؟', blank=True)
    explanation = models.TextField(verbose_name='توضیحات پروژه', max_length=6000, default=None, null=True, blank=True)
    in_home_page = models.BooleanField(blank=True, default=False, verbose_name='')
    immediate = models.BooleanField(blank=True, default=False,
                                    verbose_name='در صورت'
                                                 ' نیاز فوری علامت بزنید. لطفا تا حد امکان از این کار خودداری کنید.')
    accepted = models.BooleanField(blank=True, default=False, verbose_name='تایید شده؟')
    tag2 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag4 = models.BooleanField(blank=True, default=False, verbose_name='')
    city = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='شهر')
    province = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='استان')
    tag7 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')
    tag8 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')

    class Meta:
        verbose_name = 'پروژه کمک رسانی'
        verbose_name_plural = 'پروژه های کمک رسانی'

    def __str__(self):
        return self.title

    @staticmethod
    def autocomplete_search_fields():
        return 'title',


# !important: (self_or_hm) is very important
# if project and helper and status:project mtm
# elif helper and (field and level or skill or cities or experience: helper mtm
# elif day and time_to and time_from: project
# elif img and (ins or pro):image
class ManyToMany(models.Model):
    objects = jmodels.jManager()
    project = models.ForeignKey(Project, verbose_name='پروژه', related_name='mtms', default=None,
                                null=True, blank=True)
    helper = models.ForeignKey(User, verbose_name='مددکار', null=True, blank=True,
                               related_name='mtms', default=None)
    institute = models.ForeignKey(Institute, null=True, blank=True, default=None, related_name='mtms',
                                  verbose_name='موسسه')
    DEFINITE = 'definite'
    RESERVE = 'reserve'
    PAST = 'past'
    FAILED = 'failed'
    A_F = 'a_f'
    STATUS_CHOICES = (
        (DEFINITE, 'قطعی'),
        (RESERVE, 'رزرو'),
        (PAST, 'گذشته'),
        (FAILED, 'رد شده'),
        (A_F, 'مطلقا مردود')
    )
    status = models.CharField(choices=STATUS_CHOICES, verbose_name='وضعیت', max_length=10, default=None, blank=True,
                              null=True)  # for project many to many
    field = models.CharField(max_length=50, verbose_name='رشته', default=None, null=True, blank=True)
    BS = 'bs'
    MS = 'ms'
    PHD = 'phd'
    level_choices = (
        (BS, 'کارشناسی'),
        (MS, 'کارشناسی ارشد'),
        (PHD, 'دکترا'),
    )
    level = models.CharField(max_length=15, choices=level_choices, default=None, verbose_name='مقطع', null=True,
                             blank=True)
    the_date = jmodels.jDateField(verbose_name='تاریخ', default=None, null=True, blank=True)
    skill = models.ForeignKey(HelpType, related_name='skill_mtms', verbose_name='مهارتها', default=None, null=True,
                              blank=True)
    SA = 'sa'
    SU = 'su'
    M = 'm'
    TU = 'tu'
    W = 'w'
    TH = 'th'
    F = 'f'
    DAY_CHOICES = (
        (SA, 'شنبه'),
        (SU, 'یک شنبه'),
        (M, 'دو شنبه'),
        (TU, 'سه شنبه'),
        (W, 'چهار شنبه'),
        (TH, 'پنج شنبه'),
        (F, 'جمعه')
    )
    day = models.CharField(max_length=15, choices=DAY_CHOICES, default=None, verbose_name='روز', null=True,
                           blank=True)
    time_from = models.TimeField(max_length=15, default=None, verbose_name='از ساعت', null=True,
                                 blank=True)
    time_to = models.TimeField(max_length=15, default=None, verbose_name='تا ساعت', null=True,
                               blank=True)
    experience = models.ForeignKey(HelpType, verbose_name='تجربه های داوطلبانه', related_name='mtms',
                                   default=None,
                                   blank=True, null=True)
    image = ProcessedImageField(upload_to=get_image__i_or_p, verbose_name='عکس', default=None,
                                processors=[ResizeToFill(600, 420)], blank=True, null=True,
                                format='JPEG',
                                options={'quality': 100})
    self_or_hm = models.BooleanField(blank=True, default=False, verbose_name='اگر درست پس حاتم نتیجه گرفته.')
    I = 'image'
    T = 'time'
    S = 'skill'
    P_M = 'p_mtm'
    MTM_TYPE_CHOICES = (
        (I, 'image'),
        (T, 'time'),
        (S, 'skill'),
        (P_M, 'p_mtm')
    )
    mtm_type = models.CharField(max_length=20, choices=MTM_TYPE_CHOICES, null=True, blank=True, default=None,
                                verbose_name='برچسب نوع')
    tag3 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag4 = models.BooleanField(blank=True, default=False, verbose_name='')
    tag5 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')
    tag6 = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name='')

    class Meta:
        verbose_name = 'روابط'
        verbose_name_plural = 'روابط'
