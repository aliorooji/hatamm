from django.conf.urls import include, url
from . import views
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^faq$', TemplateView.as_view(template_name="aboutUs/faq.html")),
    url(r'^rules$', TemplateView.as_view(template_name="aboutUs/rules.html")),
    url(r'^our_persons$', TemplateView.as_view(template_name="aboutUs/our_persons.html")),
    url(r'^what_we_are$', TemplateView.as_view(template_name="aboutUs/what_we_are.html")),
    # url(r'^institute', 'Charity.views.institute'),
]
