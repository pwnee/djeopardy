from django.conf.urls import patterns, url, include
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from djeo.views import play, home #,AboutView
from djeo.models import FinalJeopardy, Contestant, UserAnswer
from djeo.forms import FinalJeopardyWager
from django.template import RequestContext
#from djeo.forms import AnswerForm
from registration.views import register

urlpatterns = patterns('',
	url(r'^$', home, name="home"),
    url('^play/(\d+)/$', play, name="play"),
    )



