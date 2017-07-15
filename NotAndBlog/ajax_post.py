from django.shortcuts import render, render_to_response, get_object_or_404
from django import forms
import json
from Charity.models import HelperProfile, Project, ManyToMany, HelpType, Case, Institute
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
import datetime
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from Charity import jalali
import jdatetime
from .models import Notification, get_image_blog
from .forms import NotificationForm
from django.core.mail import send_mail
# from django.utils import simplejson
from django.core import serializers
from django.core.files.uploadedfile import SimpleUploadedFile


def report_this(request):
    user = request.user
    if request.is_ajax():
        try:
            obj_id = request.POST.get('obj_id')
            note_type = request.POST.get('note_type')
            note_text = request.POST.get('note_text')
        except KeyError:
            return HttpResponse('Error')
        new_note = Notification()
        data = {'ok': 'f'}
        if note_text:
            if note_type == 'r_he':
                if ManyToMany.objects.filter(id=obj_id).filter(project__institute__admin=user):
                    new_note.helper = ManyToMany.objects.filter(id=obj_id).filter(
                        project__institute__admin=user).first().helper.profile
                    new_note.text = note_text
                    new_note.n_type = note_type
                    new_note.save()
                    data = {'ok': 't'}
        else:
            data = {'ok': 'not_note'}
        return HttpResponse(json.dumps(data), content_type="application/json")