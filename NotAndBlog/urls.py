from django.conf.urls import include, url
from . import views, ajax, ajax_post
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^ajax/post/report_this$', ajax_post.report_this, name='report_this'),
]
