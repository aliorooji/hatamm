import json
from .models import HelperProfile, Project, ManyToMany, HelpType, Case, Institute
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.db.models import Q
import jdatetime
from django.core.mail import send_mail


def def_del(request):
    user = request.user
    if request.is_ajax():
        try:
            obj_id = request.POST.get('obj_id')
            q = request.POST.get('q')
        except KeyError:
            return HttpResponse('Error')
        obj = Project.objects.filter(id=obj_id).filter(institute__admin=user).first()
        obj.delete()
        data = {'ok': 't'}
        return HttpResponse(json.dumps(data), content_type="application/json")


def fail_or_definite(request):
    user = request.user
    if request.is_ajax():
        try:
            obj_id = request.POST.get('obj_id')
            post_editor = request.POST.get('post_editor')
        except KeyError:
            return HttpResponse('Error')
        mtm = ManyToMany.objects.filter(id=obj_id).filter(project__institute__admin=user).first()
        a_f_count = 0
        is_finished = 'f'
        if post_editor == 'd':
            mtm.status = ManyToMany.DEFINITE
            mtm.the_date = jdatetime.date.today()
            mtm.save()
            the_helper = mtm.helper
            if the_helper.email:
                send_mail(
                    'حاتم',
                    'ثبت نام شما در پروژه' + ' ' + mtm.project.title + ' ' +
                    'قطعی گردید.',
                    'aleeoruji@gmail.com',
                    [the_helper.email],
                    fail_silently=False,
                )
        elif post_editor == "f":
            mtm.status = ManyToMany.A_F
            mtm.the_date = jdatetime.date.today()
            mtm.save()
            the_helper = mtm.helper
            if not mtm.project.mtms.filter(Q(status=ManyToMany.DEFINITE) | Q(status=ManyToMany.RESERVE)).exclude(
                    helper=None).exclude(the_date=None):
                is_finished = 't'
            if the_helper.email:
                send_mail(
                    'حاتم',
                    'سلام کاربر عزیز. ثبت نام شما در پروژه' + ' ' + mtm.project.title + ' ' +
                    'کنسل گردید.',
                    'aleeoruji@gmail.com',
                    [the_helper.email],
                    fail_silently=False,
                )
        elif post_editor in ['r', 'f_by_h']:
            mtm__project = Project.objects.filter(id=obj_id).first()
            this_mtm_user = ManyToMany.objects.filter(project__id=obj_id).filter(helper=user).filter(
                Q(status=ManyToMany.RESERVE) | Q(
                    status=ManyToMany.DEFINITE))
            this_mtm_user_a_f = ManyToMany.objects.filter(helper=user).filter(project=obj_id).filter(
                status=ManyToMany.A_F)
            if post_editor == 'r':
                if HelperProfile.objects.filter(user=user):
                    if not this_mtm_user:
                        if this_mtm_user_a_f.count() < 4:
                            new_m_t_m = ManyToMany()
                            new_m_t_m.helper = user
                            new_m_t_m.project = mtm__project
                            new_m_t_m.status = ManyToMany.RESERVE
                            new_m_t_m.the_date = jdatetime.date.today()
                            new_m_t_m.save()
                            is_finished = 't'
                            if user.email:
                                send_mail(
                                    'حاتم',
                                    'شما به عنوان رزرو در پروژه' + ' ' + mtm__project.title + ' ' + 'ثبت نام کرده اید.'
                                                                                            ' در صورت قطعی شدن'
                                                                                            ' به شما'
                                                                                            ' اعلام خواهد شد.',
                                    'hatammmail@gmail.com',
                                    [user.email],
                                    fail_silently=False,
                                )
                            if mtm__project.institute.admin.email:
                                send_mail(
                                    'حاتم',
                                    user.username + ' ' + 'در پروژه' + ' ' + mtm__project.title + ' ' + 'ثبت'
                                                                                                ' نام نموده است'
                                                                                                ' لطفا نسبت به'
                                                                                                ' تعیین وضعیت'
                                                                                                ' ایشان'
                                                                                                ' اقدام کنید.',
                                    'hatammmail@gmail.com',
                                    [mtm__project.institute.admin.email],
                                    fail_silently=False,
                                )
            elif post_editor == 'f_by_h':
                if this_mtm_user:
                    for m in this_mtm_user:
                        m.status = ManyToMany.A_F
                        m.the_date = jdatetime.date.today()
                        m.save()
                        a_f_count = this_mtm_user_a_f.count()
                        is_finished = 't'
                    if user.email:
                        send_mail(
                            'حاتم',
                            'انصراف شما از پروژه' + ' ' + mtm__project.title + ' ' +
                            'به ثبت رسید.',
                            'hatammmail@gmail.com',
                            [user.email],
                            fail_silently=False,
                        )
                    if mtm__project.institute.admin.email:
                        send_mail(
                            'حاتم',
                            user.username + 'از پروژه' + ' ' + mtm__project.title + ' ' + 'انصراف داد.',
                            'hatammmail@gmail.com',
                            [mtm__project.institute.admin.email],
                            fail_silently=False,
                        )
                pass
        p_id = 0
        if mtm:
            if mtm.project:
                p_id = mtm.project.id
        data = {'pId': p_id, 'is_finished': is_finished, 'a_f_count': a_f_count}
        return HttpResponse(json.dumps(data), content_type="application/json")
