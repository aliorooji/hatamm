from django.shortcuts import render
from .models import HelperProfile, Project, ManyToMany, HelpType, Case, Institute
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import HelperProfileForm, UserForm, ProjectForm, CaseForm, InstituteForm, MTMForm
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import jdatetime
from django.core.mail import send_mail
import googlemaps
from googlemaps.geocoding import reverse_geocode
from itertools import chain

geo_code_key = 'AIzaSyDS7eQr2JMx-2HKQN69Y_SNH-73KJp_vpw'
geo_code_client = googlemaps.Client(geo_code_key)


def home(request):
    return render(request, 'home.html', {
        '3_helper': HelperProfile.objects.filter(others_view_u=True).filter(in_home_page=True)[:3],
        '3_institute': Institute.objects.filter(in_home_page=True).filter(accepted=True)[:3],
        '3_project': Project.objects.filter(in_home_page=True).filter(institute__accepted=True)[:4]
    })


def project(request, this_id):
    user = request.user
    this = Project.objects.filter(id=this_id).first()
    if this:
        if this.institute.accepted:
            this_mtm_user = None
            this_mtm_user_a_f = None
            if not user.is_anonymous():
                this_mtm_user = ManyToMany.objects.filter(project=this).filter(helper=user).filter(
                    Q(status=ManyToMany.RESERVE) | Q(
                        status=ManyToMany.DEFINITE))
                this_mtm_user_a_f = ManyToMany.objects.filter(helper=user).filter(project=this).filter(
                    status=ManyToMany.A_F)
            h_type_list = [this.help_type]
            for h_t in this.help_type.children.all():
                h_type_list.append(h_t)
            if this.help_type.father:
                h_type_list.append(this.help_type.father)
                for h in this.help_type.father.children.all():
                    h_type_list.append(h)
            similar_this = Project.objects.filter(help_type=this.help_type).exclude(id=this.id).filter(
                end_date__range=[jdatetime.date.today(), '2500-01-01'])[:3]
            e = 3 - similar_this.count()
            similar_this2 = Project.objects.filter(help_type__in=h_type_list).exclude(help_type=this.help_type).filter(
                end_date__range=[jdatetime.date.today(), '2500-01-01'])[:e]
            e2 = 3 - (similar_this.count() + similar_this2.count())
            un_similar_this = Project.objects.exclude(help_type__in=h_type_list).filter(
                end_date__range=[jdatetime.date.today(), '2500-01-01'])[:e2]
            similar_uns_this = chain(similar_this, similar_this2, un_similar_this)
            return render(request, 'project.html', {
                'this': this,
                'similar_this': similar_uns_this,
                'this_mtm_user': this_mtm_user,
                'this_mtm_user_a_f': this_mtm_user_a_f,
            })
        else:
            return HttpResponseNotFound('<h1 class="w3-center" dir="rtl">چنین دسترسی وجود ندارد</h1>')
    else:
        return HttpResponseNotFound('<h1 class="w3-center" dir="rtl">چنین پروژه ای وجود ندارد</h1>')


@login_required
def institute(request):
    user = request.user
    if Institute.objects.filter(admin=user):
        this = user.institute.first()
        return render(request, 'institute_test.html', {
            'this': this,
            'p_mtm': ManyToMany(),
            'the_part': request.GET.get('the_part')
        })
    else:
        return HttpResponseNotFound('<h1 dir="rtl">دسترسی ندارید</h1>')


@login_required
def add_obj(request, this_id, this_type):
    user = request.user
    next_url = request.GET.get('next')
    need_case = request.POST.get('need_case')
    need_helper = request.POST.get('need_helper')
    if this_type == 'Institute':
        f_instance = Institute.objects.filter(admin=user).first()
        back_form = InstituteForm(request.POST, request.FILES, instance=f_instance)
        front_form = InstituteForm(instance=f_instance)
    elif this_type == 'Helper':
        f_instance = user.profile
        back_form = HelperProfileForm(request.POST, request.FILES, instance=f_instance)
        front_form = HelperProfileForm(instance=f_instance)
    elif this_type == 'Project':
        this_p = Project.objects.filter(id=this_id).first()
        if this_p:
            if this_p.institute.admin == user:
                f_instance = this_p
            else:
                return HttpResponseNotFound('<h1>شما قادر به ویرایش نمیباشید</h1>')
        else:
            f_instance = None
        back_form = ProjectForm(request.POST, request.FILES, instance=f_instance, user=user,
                                need_case=need_case, need_helper=need_helper)
        front_form = ProjectForm(instance=f_instance, user=user, need_case='', need_helper='')
    else:
        this_c = Case.objects.filter(id=this_id).first()
        if this_c:
            if this_c.institute.admin == user:
                f_instance = this_c
            else:
                return HttpResponseNotFound('<h1>شما قادر به ویرایش نمیباشید</h1>')
        else:
            f_instance = None
        back_form = CaseForm(request.POST, request.FILES, instance=f_instance)
        front_form = CaseForm(instance=f_instance)
    if request.method == 'POST':
        form = back_form
        if form.is_valid():
            new = form.save()
            if not f_instance:
                new.accepted = False
            new.admin = request.user
            new.user = user
            new.institute = Institute.objects.filter(admin=user).first()
            save_city_and_province(new)
            if not need_helper:
                new.min_age = None
                new.max_age = None
                new.gender = None
                new.n_t_experience = False
                new.from_home = False
            new.save()
            # user_form.save()
            # if this_type == 'Project':
            #     if next_url:
            #         the_part = next_url[0:1]
            #         return HttpResponseRedirect(next_url + '?the_part=' + the_part)
            #     else:
            # else:
            if next_url:
                the_part = next_url[0:1]
                return HttpResponseRedirect(next_url + '?the_part=' + the_part)
            else:
                return HttpResponseRedirect('/')
    else:
        form = front_form
    return render(request, 'add/add_obj.html', {
        'form': form,
        'next_url': next_url,
        'need_case_key': need_case
    })


@login_required
def add_institute(request):
    user = request.user
    next_url = request.GET.get('next')
    tem_key = None
    if Institute.objects.filter(admin=user):
        f_instance = Institute.objects.filter(admin=user).first()
    else:
        f_instance = None
    if request.method == 'POST':
        form = InstituteForm(request.POST, request.FILES, instance=f_instance)
        if form.is_valid():
            new = form.save()
            if not f_instance:
                new.accepted = False
            new.admin = request.user
            save_city_and_province(new)
            new.save()
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect('/')
        else:
            tem_key = 'f_not_valid'
    else:
        form = InstituteForm(instance=f_instance)
    return render(request, 'add/add_institute.html', {
        'form': form,
        'next_url': next_url,
        'tem_key': tem_key
    })


@login_required
def add_helper(request):
    user = request.user
    next_url = request.GET.get('next')
    tem_key = None
    f_instance = None
    if HelperProfile.objects.filter(user=user):
        f_instance = user.profile
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=user)
        form = HelperProfileForm(request.POST, request.FILES, instance=f_instance)
        if form.is_valid() and user_form.is_valid():
            new = form.save()
            save_city_and_province(new)
            new.user = user
            new.save()
            user_form.save()
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect('/')
        else:
            tem_key = 'f_not_valid'
    else:
        form = HelperProfileForm(instance=f_instance)
        user_form = UserForm(instance=user)
    return render(request, 'add/add_helper.html', {
        'form': form,
        'user_form': user_form,
        'next_url': next_url,
        'HelperProfile': HelperProfile(),
        'tem_key': tem_key
    })


@login_required
def add_case(request, this_id):
    user = request.user
    if Institute.objects.filter(admin=user):
        next_url = request.GET.get('next')
        f_instance = None
        tem_key = None
        if Case.objects.filter(id=this_id):
            this_c = Case.objects.filter(id=this_id).first()
            if this_c.institute:
                if this_c.institute.admin == user:
                    f_instance = this_c
                else:
                    return HttpResponseNotFound('<h1>شما قادر به ویرایش نمیباشید</h1>')
            else:
                return HttpResponseNotFound('<h1>شما قادر به ویرایش نمیباشید</h1>')
        if request.method == 'POST':
            form = CaseForm(request.POST, request.FILES, instance=f_instance)
            if form.is_valid():
                new = form.save()
                new.institute = Institute.objects.filter(admin=user).first()
                new.save()
                return HttpResponseRedirect(next_url)
            else:
                tem_key = 'f_not_valid'
        else:
            form = CaseForm(instance=f_instance)
        return render(request, 'add/add_case.html', {
            'form': form,
            'next_url': next_url,
            'tem_key': tem_key,
            'Case': Case()
        })
    else:
        return HttpResponseNotFound('<h1>شما قادر به ویرایش نمیباشید.</h1>')


@login_required
def add_project(request, this_id):
    user = request.user
    if Institute.objects.filter(admin=user):
        next_url = request.GET.get('next')
        the_part = next_url[0:1]
        if str(the_part).isdigit():
            next_url = next_url[1:]
        f_instance = None
        need_case_key = None
        if Project.objects.filter(id=this_id):
            this_p = Project.objects.filter(id=this_id).first()
            if this_p.institute.admin == user:
                f_instance = this_p
            else:
                return HttpResponseNotFound('<h1>شما قادر به ویرایش نمیباشید.</h1>')
        if request.method == 'POST':
            need_case = request.POST.get('need_case')
            need_case_key = need_case
            need_helper = request.POST.get('need_helper')
            form = ProjectForm(request.POST, request.FILES, instance=f_instance, user=user,
                               need_case=need_case, need_helper=need_helper)
            if form.is_valid():
                new = form.save()
                new.institute = Institute.objects.filter(admin=user).first()
                save_city_and_province(new)
                if not need_helper:
                    new.min_age = None
                    new.max_age = None
                    new.gender = None
                    new.n_t_experience = False
                    new.from_home = False
                new.save()
                return HttpResponseRedirect(next_url + '?the_part=' + the_part)
        else:
            form = ProjectForm(instance=f_instance, user=user, need_case='', need_helper='')
        return render(request, 'add/add_project_t.html', {
            'form': form,
            'next_url': next_url,
            'need_case_key': need_case_key,
            'HelperProfile': HelperProfile(),
        })
    else:
        return HttpResponseNotFound('<h1>شما قادر به ویرایش نمیباشید.</h1>')


@login_required
def helper_profile(request):
    user = request.user
    if HelperProfile.objects.filter(user=user):
        this = HelperProfile.objects.filter(user=user).first()
        tem_key = None
        if request.method == 'POST':
            post_editor = request.POST.get('post_editor')
            if post_editor in ['education', 'skill', 'city']:
                form = MTMForm(request.POST, request.FILES, reagent='helper_profile')
                if form.is_valid():
                    new = form.save()
                    new.helper = this.user
                    if post_editor == 'education':
                        if not ManyToMany.objects.filter(helper=this.user).filter(
                                field=form.cleaned_data['field']).filter(level=form.cleaned_data['level']):
                            new.save()
                    elif post_editor == 'skill':
                        if not ManyToMany.objects.filter(helper=this.user).filter(skill=form.cleaned_data['skill']):
                            new.save()
                    elif post_editor == 'city':
                        if not ManyToMany.objects.filter(helper=this.user).filter(
                                cities_wants_to_go=form.cleaned_data['cities_wants_to_go']):
                            new.save()
            elif post_editor == 'dis_p':
                # dis_p_id = request.POST.get('this-c-p-input')
                # if ManyToMany.objects.filter(id=dis_p_id).filter(helper=this.user):
                #     for mtm in ManyToMany.objects.filter(id=dis_p_id).filter(helper=this.user):
                #         mtm.delete()
                this_mtm_user = ManyToMany.objects.filter(project__id=this.id).filter(helper=user).filter(
                    Q(status=ManyToMany.RESERVE) | Q(status=ManyToMany.DEFINITE))
                if this_mtm_user:
                    for mtm in this_mtm_user:
                        mtm.status = ManyToMany.A_F
                        mtm.the_date = jdatetime.date.today()
                        mtm.save()
                    tem_key = 'dis_mtm'
                    if user.email:
                        send_mail(
                            'حاتم',
                            'انصراف شما از پروژه' + ' ' + this.title + ' ' +
                            'به ثبت رسید.',
                            'aleeoruji@gmail.com',
                            [user.email],
                            fail_silently=False,
                        )
                    if this.institute.admin.email:
                        send_mail(
                            'حاتم',
                            user.username + 'از پروژه' + ' ' + this.title + ' ' + 'انصراف داد.',
                            'aleeoruji@gmail.com',
                            [this.institute.admin.email],
                            fail_silently=False,
                        )

        else:
            pass
        return render(request, 'helper_profile.html', {
            'this': this,
            'h_p_form': HelperProfileForm(instance=this),
            'h_mtm_form': MTMForm(reagent='helper_profile'),
            'p_mtm': ManyToMany(),
            'tem_key': tem_key,
        })
    else:
        return render(request, 'helper_profile.html', {
        })


def pro_all(request, query):
    if query in ['Project', 'Helper', 'Institute']:
        return render(request, 'project_all.html', {
            'institute_list': Institute.objects.all(),
            'pro_list': Project.objects.all(),
            'query': query,
        })
    else:
        return HttpResponseNotFound('<h1>چنین آدرسی وجود ندارد</h1>')


def view_institute(request, this_id):
    if Institute.objects.filter(id=this_id):
        this = Institute.objects.filter(id=this_id).first()
        l = this.profile_image.url[14:10000]
        if this.accepted:
            return render(
                request, 'view_institute.html', {
                    'this': this,
                    'this_current_ps': this.projects.filter(
                        end_date__range=[jdatetime.date.today(), '2200-01-01'])[:4],
                    'this_past_ps': this.projects.filter(
                        end_date__range=['2000-01-01', jdatetime.date.today()])[:2],
                    'this_images': this.mtms.filter(mtm_type=ManyToMany.I),
                    'l': l
                })
        else:
            return HttpResponseNotFound('<h1>غیر قابل دست رسی</h1>')

    else:
        return HttpResponseNotFound('<h1>چنین موسسه ای وجود ندارد</h1>')


def all_institute(request):
    institute_all = Institute.objects.filter(accepted=True)
    all_ins_page = request.GET.get('all_ins_page', '1')
    all_ins_paginator = Paginator(institute_all, 14)
    ins = Institute.objects.first()
    try:
        all_ins_list = all_ins_paginator.page(all_ins_page)
    except PageNotAnInteger:
        all_ins_list = all_ins_paginator.page(1)
    except EmptyPage:
        all_ins_list = all_ins_paginator.page(all_ins_paginator.num_pages)
    return render(request, 'all_institute_test.html', {
        'all_ins_list': Institute.objects.all(),
        'ins': ins
    })


def all_h_or_i(request, query):
    return render(request, 'all_h_or_i.html', {
        'query': query
    })


def before_all_hip(request, query):
    if query in ["Project", "Helper", "Institute"]:
        return render(request, 'before_all_hip.html', {
            'query': query,
            'cities_list': ['استان خراسان رضوی', 'استان خراسان شمالی', 'استان خراسان جنوبی', 'استان آذربایجان شرقی',
                            'استان آذربایجان غربی',
                            'استان اردبیل',
                            'استان اصفهان', 'استان البرز', 'استان ایلام', 'استان بوشهر', 'استان تهران',
                            'استان چهارمحال و بختیاری', 'استان خوزستان', 'استان زنجان',
                            'استان سمنان', 'استان سیستان و بلوچستان', 'استان فارس', 'استان قزوین', 'استان قم',
                            'استان کردستان', 'استان کرمان', 'استان کرمانشاه',
                            'استان کهگیلویه و بویراحمد', 'استان گلستان', 'استان گیلان', 'استان لرستان',
                            'استان مازندران', 'استان مرکزی', 'استان هرمزگان', 'استان همدان',
                            'استان یزد']
        })
    else:
        return HttpResponseNotFound('<h1>چنین آدرسی وجود ندارد</h1>')


def view_helper(request, this_id):
    this = HelperProfile.objects.filter(id=this_id).first()
    if this.others_view_u:
        return render(request, 'view_helper.html', {
            'this': this
        })
    else:
        return HttpResponseNotFound('<h1 class="c-font-mehr w3-red">')


def join_as(request):
    return render(request, 'join_as.html', {
    })


def what_you_want(request):
    return render(request, 'alaki.html', {
        # 'user': request.user
    })


def continue_fill(request):
    return render(request, 'continue_fill.html', {
        "tem_key": request.GET.get('tem_key')
    })


def save_city_and_province(new):
    reversed_data = reverse_geocode(latlng=(new.lat, new.lng), client=geo_code_client)
    for i in reversed_data:
        address_components = i.get('address_components')
        for j in address_components:
            if 'administrative_area_level_1' in j.get('types'):
                new.province = j.get('long_name')
