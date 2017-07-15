from django import template
# from program.models import Program,Message
import jdatetime
from Charity.models import Project, Institute, HelpType, ManyToMany
from django.db.models import Q

register = template.Library()


@register.filter
def get_tuple_item(tup, key):
    dicti = dict(tup)
    return dicti[key]


@register.assignment_tag
def obj_by_id(o_id, query):
    obj = None
    if query == 'project':
        obj = Project.objects.filter(id=o_id).first()
    elif query == 'institute':
        obj = Institute.objects.filter(id=o_id).first()
    elif query == 'help_type':
        obj = HelpType.objects.filter(id=o_id).first()
    return obj


@register.assignment_tag
def past_or_not(date):
    if (jdatetime.date.today() - date) > jdatetime.timedelta(days=0):
        return True
    else:
        return None


@register.assignment_tag
def mtm_list(obj_id, mtm_type, id_for):
    if mtm_type == "p_h":
        if id_for == "p":
            mtms = ManyToMany.objects.filter(project__id=obj_id).exclude(helper=None).filter(
                Q(status=ManyToMany.RESERVE) | Q(
                    status=ManyToMany.DEFINITE))
            return mtms


@register.assignment_tag
def img_use_by_static(img_url):
    img_url = img_url[14:100000]
    return img_url


@register.assignment_tag
def types_by_father_with_child(f):
    if f == 0:
        type_list = HelpType.objects.filter(father=None).exclude(children=None)
    else:
        type_list = HelpType.objects.filter(father__id=f).exclude(children=None)
    return type_list


@register.assignment_tag
def types_by_father_without_child(f):
    if f == 0:
        type_list = HelpType.objects.filter(father=None).filter(children=None)
    else:
        type_list = HelpType.objects.filter(father__id=f).filter(children=None)
    return type_list
