from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import HelperProfile, Project, ManyToMany, HelpType, Case, Institute
# import datetime
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from Charity import jalali
import jdatetime


class HelperProfileForm(forms.ModelForm):
    class Meta:
        model = HelperProfile
        exclude = ['user', "in_home_page", "min_age", "accepted",
                   "city", "city", "province", "city", "province",
                   'tag1', 'tag6', 'tag5', 'tag4', 'instagram', 'facebook', 'twitter',
                   'telegram', 'monthly_cooperation_time']

    def clean_phone_num(self):
        if check_phone_num(self.cleaned_data['phone_num']):
            return self.cleaned_data['phone_num']

    def clean_national_code(self):
        if check_national_code(self.cleaned_data['national_code']):
            return self.cleaned_data['national_code']

    def __init__(self, *args, **kwargs):
        super(HelperProfileForm, self).__init__(*args, **kwargs)
        self.fields['lat'].required = True
        self.fields['lng'].required = True


class MTMForm(forms.ModelForm):
    class Meta:
        model = ManyToMany
        exclude = ['']

    def __init__(self, *args, **kwargs):
        reagent = kwargs.pop('reagent')
        super(MTMForm, self).__init__(*args, **kwargs)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['national_code', 'job', 'explanation', 'institute']

    def clean_national_code(self):
        if check_national_code(self.cleaned_data['national_code']):
            return self.cleaned_data['national_code']

    def __init__(self, *args, **kwargs):
        reagent_id = kwargs.pop('reagent_id', None)
        super(CaseForm, self).__init__(*args, **kwargs)
        if reagent_id != 0:
            del self.fields['institute']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ["accepted", "city", 'tag7', "province", "city",
                   "province", 'tag8', "in_home_page", "in_home_page",
                   'tag2', 'tag4']

    def clean_min_age(self):
        if check_min_age(self.cleaned_data["min_age"]):
            return self.cleaned_data["min_age"]

    def clean_max_age(self):
        if check_max_age(self.cleaned_data["max_age"]):
            return self.cleaned_data["max_age"]

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        if 'start_date' in cleaned_data.keys() and 'end_date' in cleaned_data.keys():
            if check_start_end_date(self.cleaned_data['start_date'], self.cleaned_data['end_date']):
                pass
            else:
                self.add_error('end_date', forms.ValidationError(_('تاریخ پایان نباید قبل از تاریخ شروع باشد')))
        if 'max_age' in cleaned_data.keys():
            if 'min_age' in cleaned_data.keys():
                if check_min_max_age(self.cleaned_data['min_age'], self.cleaned_data['max_age']):
                    pass
                else:
                    self.add_error('max_age',
                                   forms.ValidationError(_('کمترین سن ممکن نمی تواند بیش از کم ترین سن ممکن باشد.')))
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        reagent_id = kwargs.pop('reagent_id', None)
        user = kwargs.pop('user')
        need_case = kwargs.pop('need_case')
        need_helper = kwargs.pop('need_helper')
        super(ProjectForm, self).__init__(*args, **kwargs)
        del self.fields['status']
        del self.fields['institute']
        self.fields['case'].queryset = user.institute.first().cases.all()
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True
        self.fields['lat'].required = True
        self.fields['lng'].required = True
        if need_case:
            self.fields['case'].required = True
        if need_helper:
            self.fields['min_age'].required = True
            self.fields['max_age'].required = True
            # def __init__(self, *args, **kwargs):
            #     current_user = kwargs.pop('user')
            #     super(BookForm, self).__init__(*args, **kwargs)
            #     self.fields['categories'].queryset = Categories.objects.filter(creator=current_user)


class InstituteForm(forms.ModelForm):
    class Meta:
        model = Institute
        exclude = ["accepted", "city", "province", "city", "province",
                   'n_score', 'accepted', "min_age", "in_home_page",
                   'admin', 'tag1', 'tag5', 'tag6', 'telegram','twitter',
                   'facebook', 'instagram', 'email', 'phone_num2', 'site_address'
                   ]

    def clean_agent_num(self):
        if check_phone_num(self.cleaned_data['agent_num']):
            return self.cleaned_data['agent_num']

    def __init__(self, *args, **kwargs):
        this_id = kwargs.pop('this_id', None)
        super(InstituteForm, self).__init__(*args, **kwargs)
        self.fields['lat'].required = True
        self.fields['lng'].required = True
        # if this_id != 0:
        #     del self.fields['national_code']
        #     del self.fields['patent_num']


def check_national_code(national_code):
    a = national_code
    if a.isdigit():
        if len(a) == 8:
            a = '00' + a
        if len(a) == 9:
            a = '0' + a
        print(a)
        if len(a) == 10:
            r = 0
            for i in range(0, 9):
                r1 = int(a[i]) * (10 - i)
                r = r1 + r
            c = r % 11
            if (int(a[9]) == 1) and (c == 1):
                return True
            elif (int(a[9]) == 0) and (c == 0):
                return True
            elif (int(a[9]) == 11 - c):
                return True
            else:
                raise forms.ValidationError(_('کد ملی وارد شده معتبر نیست'))
        else:
            raise forms.ValidationError(_('کد ملی وارد شده معتبر نیست'))
    else:
        raise forms.ValidationError(_('کد ملی وارد شده باید عدد باشد'))


def check_phone_num(phone_num):
    a = phone_num
    if a:
        if a.isdigit():
            if (len(a) == 10 and int(a[0]) == 9):
                a = '0' + a
            if (len(a) == 11):
                if (int(a[0]) == 0 and int(a[1]) == 9):
                    return True
                else:
                    raise forms.ValidationError(_('شماره تلفن وارد شده متعلق به ایران نمی باشد'))
            else:
                raise forms.ValidationError(_('شماره تلفن وارد شده صحیح نمی باشد'))
        else:
            raise forms.ValidationError(_('شماره تلفن باید عدد باشد'))


def is_not_date_in_past(date):
    if date:
        if (date - jdatetime.date.today()) > jdatetime.timedelta(days=-1):
            return True
        else:
            raise forms.ValidationError(_('تاریخ گذشته قابل قبول نیست'))


def check_min_age(mn):
    if mn:
        if 9 < mn < 73:
            return True
        else:
            raise forms.ValidationError(_('لطفا یک عدد بین 10 تا 72 وارد کنید.'))
    else:
        return True


def check_max_age(mx):
    if mx:
        if 11 < mx < 121:
            return True
        else:
            raise forms.ValidationError(_('لطفا یک عدد بین ۷ تا 120 وارد کنید.'))
    else:
        return True


def check_start_end_date(start_date, end_date):
    if start_date and end_date:
        if (end_date - start_date) > jdatetime.timedelta(days=-1):
            return True
        else:
            return None
    else:
        return None


def check_min_max_age(min_age, max_age):
    if min_age and max_age:
        if max_age - min_age >= 0:
            return True
        else:
            return None
    else:
        return True

# def check_lat_lng(s, q):
#     lt = s.cleaned_data['lat']
#     lg = s.cleaned_data['lng']
#     if lt and lg:
#         if q == "Project":
#             l = Project.objects.filter(lat=lt).filter(lng=lg).exclude(pk=s.instance.pk).first()
#         elif q == "Institute":
#             l = Institute.objects.filter(lat=lt).filter(lng=lg).exclude(pk=s.instance.pk).first()
#         else:
#             l = HelperProfile.objects.filter(lat=lt).filter(lng=lg).exclude(pk=s.instance.pk).first()
#         if l:
#             return None
#         else:
#             return True
#     return None

# def check_cases(cases):
#     base_gender = cases.first().gender
#     for case in cases:
#         if case.gender != base_gender:
#             raise forms.ValidationError(_('همه نفرات باید دارای یک جنسیت باشند'))
#     else:
#         return True
