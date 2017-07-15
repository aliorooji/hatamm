from .cities import all_cities
import json
from .models import HelperProfile, Project, ManyToMany, HelpType, Case, Institute
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q
import jdatetime
import googlemaps
from math import pow

geo_code_key = 'AIzaSyDS7eQr2JMx-2HKQN69Y_SNH-73KJp_vpw'
geo_code_client = googlemaps.Client(geo_code_key)


def get_obj(request):
    if request.is_ajax():
        try:
            obj_page = request.GET.get('obj_page', '')
            query = request.GET.get('query')
        except KeyError:
            return HttpResponse('Error')  # incorrect post
        all_obj = HelperProfile.objects.filter(others_view_u=True)
        if query == 'Institute':
            all_obj = Institute.objects.filter(accepted=True)
        if all_obj:
            obj_paginator = Paginator(all_obj, 14)
            try:
                obj_s = obj_paginator.page(obj_page)
            except PageNotAnInteger:
                obj_s = obj_paginator.page(1)
            except EmptyPage:
                obj_s = obj_paginator.page(obj_paginator.num_pages)
            if int(obj_page) > obj_s.paginator.num_pages:
                data = {'empty': 'empty'}
            else:
                obj_list = []
                if query == 'Helper':
                    for h in obj_s:
                        h_img_url = '/static/this_project/img/persons-img/person1.png'
                        if h.profile_image:
                            h_img_url = h.profile_image.url[6:]
                        obj_list.append(
                            {"h_id": h.id, "username": h.user.username, "job": h.job, "about_you": h.about_you,
                             "h_img_url": h_img_url,
                             })
                else:
                    for i in obj_s:
                        i_img_url = '/static/this_project/img/hatam-camp/jahadi2.jpg'
                        if i.profile_image:
                            i_img_url = i.profile_image.url[6:]
                        obj_list.append(
                            {"i_id": i.id, "title": i.title, "date": i.phone_num, "explanation": i.explanation,
                             "i_img_url": i_img_url,
                             })
                data = {'obj_list': obj_list,
                        'list_has_next': obj_s.has_next(),
                        }
        else:
            data = {'empty': 'empty'}
        return HttpResponse(json.dumps(data), content_type="application/json")


def pro_all__filter_for_test(request):
    if request.is_ajax():
        try:
            center_lat = request.GET.get('center_lat')
            center_lng = request.GET.get('center_lng')
            t_f_id = request.GET.get('t_f_id')
            province = request.GET.get('c_f_input')
            i_id = request.GET.get('i_id')
            s1_date = request.GET.get('s1_date')
            s2_date = request.GET.get('s2_date')
            e1_date = request.GET.get('e1_date')
            e2_date = request.GET.get('e2_date')
            is_from_h = request.GET.get('is_from_h')
            radius = request.GET.get('radius')
            page = request.GET.get('page')
        except KeyError:
            return HttpResponse('Error')  # incorrect post
        obj_list = []
        e1 = jdatetime.date.today()
        e2 = '2500-01-01'
        s1 = '2000-01-01'
        s2 = '2500-01-01'
        if e1_date:
            e1 = e1_date
        if e2_date:
            e2 = e2_date
        if s1_date:
            s1 = s1_date
        if s2_date:
            s2 = s2_date
        all_project = Project.objects.filter(institute__accepted=True).filter(
            start_date__range=[s1, s2]).filter(end_date__range=[e1, e2])
        t_f_id = int(t_f_id)
        if t_f_id <= 0:
            pass
        else:
            var_h_t = HelpType.objects.filter(id=t_f_id).first()
            here_t_f_list = [var_h_t]
            for h in here_t_f_list:
                if h.children.all():
                    for t in h.children.all():
                        here_t_f_list.append(t)
            all_project = all_project.filter(help_type_id__in=here_t_f_list)
        if i_id:
            if str(i_id).isdigit():
                i_id = int(i_id)
                if i_id <= 0:
                    pass
                else:
                    all_project = all_project.filter(institute_id=i_id)
            else:
                pass
        if is_from_h == 'ok':
            all_project = all_project.filter(from_home=True)
        if is_from_h == 'no':
            all_project = all_project.filter(from_home=False)
        list_by_loc = []
        if province:
            for item in all_project.filter(province=province):
                list_by_loc.append(item)
        elif center_lat and center_lng and radius:
            for item in all_project:
                if item.lat and item.lng:
                    x = pow((item.lat - float(center_lat)), 2)
                    y = pow((item.lng - float(center_lng)), 2)
                    j = pow(x + y, 1 / 12)
                    radius = float(radius)
                    if j < radius:
                        list_by_loc.append(item)
        else:
            for item in all_project:
                list_by_loc.append(item)
        obj_paginator = Paginator(list_by_loc, 14)
        try:
            project_s = obj_paginator.page(page)
        except PageNotAnInteger:
            project_s = obj_paginator.page(1)
        except EmptyPage:
            project_s = obj_paginator.page(obj_paginator.num_pages)
        if int(page) > project_s.paginator.num_pages:
            data = {'empty': 'empty'}
        else:
            for p in project_s:
                img_url = '/static/this_project/img/hatam-camp/jahadi2.jpg'
                if p.image:
                    img_url = p.image.url[6:]
                elif p.institute.profile_image:
                    img_url = p.institute.profile_image.url[6:]
                obj_list.append(
                    {"title": p.title, "id": p.id, "sentence": p.sentence, "ins_id": p.institute.id,
                     "img_url": img_url,
                     "ins_title": p.institute.title, "h_t_title": p.help_type.title, "f_home": p.from_home,
                     "explanation": p.explanation
                     })
            data = {'obj_list': obj_list, 'has_next': project_s.has_next()}
        return HttpResponse(json.dumps(data), content_type="application/json")


def get__help_type(request):
    if request.is_ajax():
        try:
            t_f_id = request.GET.get('t_f_id')
        except KeyError:
            return HttpResponse('Error')  # incorrect post
        h_type_list = []
        if str(t_f_id).isdigit():
            t_f_id = int(t_f_id)
            if t_f_id <= 0:
                types = HelpType.objects.filter(father=None)
            else:
                f = HelpType.objects.filter(id=t_f_id).first()
                types = f.children.all()
                if f.father:
                    h_type_list.append({'h_t_id': f.father.id, 'h_t_title': f.father.title, 'h_t_status': 2})
                    h_type_list.append({'h_t_id': f.id, 'h_t_title': f.title, 'h_t_status': 0, 'num': num_of_projects(f)})
                else:
                    h_type_list.append({'h_t_id': 0, 'h_t_title': 'همه', 'h_t_status': 2})
                    h_type_list.append({'h_t_id': f.id, 'h_t_title': f.title, 'h_t_status': 0, 'num': num_of_projects(f)})
            for t in types:
                h_t_status = 0
                if t.children.all():
                    h_t_status = 1
                obj = {'h_t_id': t.id, 'h_t_title': t.title, 'h_t_status': h_t_status, 'num': num_of_projects(t)}
                h_type_list.append(obj)
        data = {'h_type_list': h_type_list}
        return HttpResponse(json.dumps(data), content_type="application/json")


def num_of_projects(t):
    ch_list = [t]
    for ch in ch_list:
        for c in ch.children.all():
            ch_list.append(c)
    num = Project.objects.filter(help_type__in=ch_list).filter(
        end_date__range=[jdatetime.date.today(), '2500-01-01']).filter(institute__accepted=True).count()
    return num


def need_helper_test(request):
    if request.is_ajax():
        try:
            s_t_id = request.GET.get('s_t_id')
        except KeyError:
            return HttpResponse('Error')  # incorrect post
        if not s_t_id:
            return HttpResponse('Error')
        else:
            if str(s_t_id).isdigit():
                s_t_id = int(s_t_id)
                if s_t_id <= 0:
                    return HttpResponse('Error')
                else:
                    m_father = HelpType.objects.filter(id=s_t_id).first()
                    f_list = [HelpType.objects.filter(id=s_t_id).first()]
                    for h_t in f_list:
                        if h_t.father:
                            if h_t.father.father:
                                f_list.append(h_t.father)
                            else:
                                m_father = h_t.father
                    if m_father == HelpType.objects.filter(title='اهدای خدمات').first():
                        data = {'need_helper': 'yes'}
                    else:
                        data = {'need_helper': None}
                    return HttpResponse(json.dumps(data), content_type="application/json")


def get__city(request):
    if request.is_ajax():
        data = {'city_list': all_cities}
        return HttpResponse(json.dumps(data), content_type="application/json")


def get_type_or_tooltip(request):
    if request.is_ajax():
        try:
            t_id = request.GET.get('t_id')
        except KeyError:
            return HttpResponse('Error')
        h_t = HelpType.objects.filter(id=t_id).first()
        if t_id == '0':
            h_t_all = HelpType.objects.filter(father=None)
        else:
            h_t_all = h_t.children.all()
        h_t_img = '/static/this_project/img/etc/1494592005_Build.png'
        h_t_list = []
        n = Project.objects.filter(help_type=h_t).filter(
            end_date__range=[jdatetime.date.today(), '2500-01-01']).filter(institute__accepted=True).count()
        if h_t_all:
            for t in h_t_all:
                if t.image:
                    h_t_img = t.image.url[6:]
                ch_list = [t]
                for item in ch_list:
                    for c in item.children.all():
                        ch_list.append(c)
                num = Project.objects.filter(help_type__in=ch_list).filter(
                    end_date__range=[jdatetime.date.today(), '2500-01-01']).filter(institute__accepted=True).count()
                n += num
                if t.children.all():
                    w_ch_or_n = 'y'
                else:
                    w_ch_or_n = 'n'
                h_t_list.append(
                    {'t__i': t.id, 't__title': t.title, 'h_t_img': h_t_img, 'num': num, 'w_ch_or_n': w_ch_or_n})
        if h_t:
            if h_t.image:
                h_t_img = h_t.image.url[6:]
            h_t_list.append({'t__i': h_t.id, 't__title': h_t.title, 'h_t_img': h_t_img, 'num': n, 'w_ch_or_n': 'n'})
        data = {'h_t_list': h_t_list}
        return HttpResponse(json.dumps(data), content_type="application/json")


def get_ins_pro(request):
    if request.is_ajax():
        try:
            i_id = request.GET.get('i_id')
            get_pro_editor = request.GET.get('get_pro_editor')
        except KeyError:
            return HttpResponse('Error')
        if get_pro_editor in ['1', '2', '3', '4', '5']:
            p_all = Project.objects.filter(institute__id=i_id)
            if get_pro_editor == '1':
                p_list = p_all.filter(accepted=False).filter(
                    start_date__range=[jdatetime.date.today(), '2500-01-01']).exclude(status=Project.S)
            elif get_pro_editor == '2':
                p_list = p_all.filter(accepted=True).filter(
                    start_date__range=[jdatetime.date.today(), '2500-01-01']).exclude(status=Project.S)
            elif get_pro_editor == '3':
                p_list = p_all.filter(accepted=True).filter(
                    start_date__range=['2000-01-01', jdatetime.date.today()]).filter(
                    end_date__range=[jdatetime.date.today(), '2500-01-01']).exclude(status=Project.S)
            elif get_pro_editor == '4':
                p_list = p_all.filter(accepted=True).filter(
                    end_date__range=['2000-01-01', jdatetime.date.today()]).exclude(status=Project.S)
            else:
                p_list = p_all.filter(accepted=True).filter(
                    start_date__range=['2000-01-01', jdatetime.date.today()]).filter(status=Project.S)
            pro_list = []
            if p_list:
                for p in p_list:
                    p_has__h_mtm = 'f'
                    if p.mtms.filter(Q(status=ManyToMany.DEFINITE) | Q(status=ManyToMany.RESERVE)).exclude(
                            helper=None).exclude(the_date=None):
                        p_has__h_mtm = 't'
                    pro_list.append({'p_id': p.id, 'p_has__h_mtm': p_has__h_mtm, 'p_title': p.title})
                data = {'pro_list': pro_list}
            else:
                data = {'empty': 'empty'}
        else:
            data = {'empty': 'empty'}
        return HttpResponse(json.dumps(data), content_type="application/json")


def get_p_mtms(request):
    if request.is_ajax():
        try:
            mtm__p_id = request.GET.get('mtm__p_id')
        except KeyError:
            return HttpResponse('Error')
        p = Project.objects.filter(institute__admin=request.user).filter(id=mtm__p_id).first()
        mtms = p.mtms.filter(Q(status=ManyToMany.DEFINITE) | Q(status=ManyToMany.RESERVE)).exclude(
            helper=None).exclude(the_date=None)
        if mtms:
            mtm_list = []
            for mtm in mtms:
                mtm_list.append({'helper_username': mtm.helper.username, 'helper_phone': mtm.helper.profile.phone_num,
                                 'status': mtm.status, 'mtm_id': mtm.id})
            data = {"mtm_list": mtm_list}
        else:
            data = {'empty': 'empty'}
        return HttpResponse(json.dumps(data), content_type="application/json")
