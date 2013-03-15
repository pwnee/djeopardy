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

def stub(request, *args, **kwargs):
    return HttpResponse('stub viadsfew', mimetype="text/plain")

def play_random(user):
	#Get FJ that User has answered
	user_answer = UserAnswer.objects.all().get(user=user)
	# Now we have a query set with all answered UserObjects
	for entry in user_answers:
		if user_answers[entry].get('question'):
			pass
	fj_objects = FinalJeopardy.obects.exclude(id=1)




def answer(request):
	fj_object = FinalJeopardy.objects.get(id=1)
	fj_answer = FinalJeopardyWager()
	contestant = Contestant.objects.get(id=1)
	print "in answer method"
	if request.method == 'POST':
		answer = request.POST.get('answer')
		print answer 
		print fj_object.correct_answer
		if answer == fj_object.correct_answer:
			contestant.update(total_cash = total_cash + wager)
			return render_to_response('base.html', context_instance=RequestContext(request))
		else:
			return render_to_response('djeo/play.html', {'fj':fj_object, 'fj_answer':fj_answer}, context_instance=RequestContext(request))
	return render_to_response('djeo/play.html', {'fj':fj_object, 'fj_answer':fj_answer}, context_instance=RequestContext(request))


def final_jeo(request):
    fj_object = FinalJeopardy.objects.get(id=1)    
    fj_answer = FinalJeopardyWager()
    #print fj_answer
    if request.method == 'POST':
    	fj_answer.wager = request.POST.get('wager')
    	fj_answer.answer = request.POST.get('answer')
    	fj_answer.correct_answer = fj_object.correct_answer
    	if fj_answer.is_valid():
    		print "is_validasdfsafd"
    		if fj_answer.is_answer_correct():
    			print "CORRECT"
		return HttpResponseRedirect('/result/')

    return render_to_response('djeo/fj.html', {'fj':fj_object, 'fj_a': fj_answer}, context_instance=RequestContext(request))

urlpatterns = patterns('',
	url(r'^$', home, name="home"),
    #url(r'^answer/$', answer, name="answer"),
    #url(r'^play/(?P<fj_id>\d+)/$', 'djeo.views.play2'),
    #url(r'^play/$', play, name="play"),   
    url('^play/(\d+)/$', play, name="play"),
    #rl(r'^/result/$', stub, name="fj_result"),
    #url(r'^about/', AboutView.as_view()),
    #url(r'^play2/[0-9]$',)
    )



