# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
from djeo.models import FinalJeopardy
from django.conf.urls import patterns, url, include
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from djeo.models import FinalJeopardy, Contestant, UserAnswer
from djeo.forms import FinalJeopardyWager
from django.template import RequestContext
from random import choice
from registration.views import register
from django.core.exceptions import ObjectDoesNotExist

def get_unasked_question_id(user, fj_id=1):
    user_answers = UserAnswer.objects.filter(user=user).values('question')
    total_questions = FinalJeopardy.objects.all()
    if user_answers == total_questions:
        return False
    answered_questions = []
    for answer in user_answers:
        answered_questions.append(int(answer['question']))
    
    #if the user hasn't answered, great, allow it    
    fj_id = int(fj_id)
    if fj_id not in answered_questions:        
        return fj_id
    else:
        #Find question user has not answered       
        unanswered_questions = FinalJeopardy.objects.exclude(id__in=answered_questions)[:50]     
        random_question =  choice(unanswered_questions)        
        return random_question.id

def is_contestant(user):
    try: 
        Contestant.objects.get(user=user)
    except ObjectDoesNotExist:        
        new_contestant = Contestant(user_id=user.id, first_name = user.username, total_cash = 25000, wager=0 )
        new_contestant.save()

def wager(request,fj_id=1):
    pass
def answer(request, fj_id=1):
    pass
    
def play(request, fj_id=1):
    user = request.user
    is_contestant(user)

    fj_id = get_unasked_question_id(user, fj_id)
    fj_object = FinalJeopardy.objects.get(id=fj_id)
       
    user_answers = UserAnswer.objects.filter(user=user).values('question')
    
    contestant = Contestant.objects.get(user=user)  
    fj_answer = FinalJeopardyWager()
    user_answer = UserAnswer()

    if request.method == 'POST' and request.POST.get('wager'):
        wager = request.POST.get('wager')
        Contestant.objects.filter(user=user).update(wager = wager)
        return render_to_response('djeo/fj.html', {'fj':fj_object, 'fj_answer':fj_answer, 'contestant': contestant}, context_instance=RequestContext(request))  
    
    if request.method == 'POST' and request.POST.get('answer'):
        answer = request.POST.get('answer')
        print answer
        total_cash = contestant.total_cash
        wager = contestant.wager
        print total_cash
        print wager
        #USER ANSWERED THIS QUESTION: ADD THAT ROW TO THE DB        
        if answer == fj_object.correct_answer:
            #CORRECT ANSWER
            Contestant.objects.filter(user=user).update(total_cash = total_cash + wager)
            contestant.total_cash = (total_cash + wager)
            Contestant.objects.filter(user=user).update(wager = 0)
            question = fj_object.id
            print "question id", question
            new_user_answer = UserAnswer(user=user, question=question, answered=1, correct=1)
            new_user_answer.save()
            next_fj_id = get_unasked_question_id(user)
            print "next id:", next_fj_id
            next_fj_object =  FinalJeopardy.objects.get(id=next_fj_id)
            return render_to_response('djeo/correct.html', {'contestant': contestant, 'fj':fj_object, 'fj_answer':fj_answer, 'next_fj_object':next_fj_object }, context_instance=RequestContext(request))
        else:
            #WRONG!
            if total_cash - wager <= 0:
                print "less than total, reset to 25000"
                Contestant.objects.filter(user=user).update(total_cash = 25000)
                Contestant.objects.filter(user=user).update(wager = 0)
                wager = 0
            elif total_cash > 0:
                print"total cash", total_cash
                Contestant.objects.filter(user=user).update(total_cash = total_cash - wager)
                contestant.total_cash = (total_cash - wager)
                Contestant.objects.filter(user=user).update(wager = 0)
                question = fj_object.id
                print "question id", question
            new_user_answer = UserAnswer(user=user, question=question, answered=1, correct=0)
            new_user_answer.save()
            next_fj_id = get_unasked_question_id(user)
            print "next: ", next_fj_id
            next_fj_object =  FinalJeopardy.objects.get(id=next_fj_id)

            return render_to_response('djeo/wrong.html', {'contestant': contestant, 'fj':fj_object, 'fj_answer':fj_answer, 'next_fj_object':next_fj_object}, context_instance=RequestContext(request))
    return render_to_response('djeo/play.html', {'fj':fj_object, 'fj_answer':fj_answer, 'contestant': contestant}, context_instance=RequestContext(request))

def home(request):
    user = request.user
    is_contestant(user)
    new_question_id = get_unasked_question_id(user)
    fj_object = fj_object = FinalJeopardy.objects.get(id=new_question_id)
    return render_to_response('base.html', {'fj_object':fj_object}, context_instance=RequestContext(request))



def play2(request, fj_id=1):
    user = request.user
    print fj_id     
    #fj_id = get_unasked_question_id(user, fj_id)
    fj_object = FinalJeopardy.objects.get(id=fj_id)
    #grab another fj for the user to continue on to:
    next_fj_id = get_unasked_question_id(user, 1)
    next_fj_object = FinalJeopardy.objects.get(id=next_fj_id)
    print next_fj_object
    user_answers = UserAnswer.objects.filter(user=user).values('question')
    
    contestant = Contestant.objects.get(user=user)  
    fj_answer = FinalJeopardyWager()
    user_answer = UserAnswer()
    
    if request.method == 'POST' and request.POST.get('wager'):
        wager = request.POST.get('wager')
        Contestant.objects.filter(id=1).update(wager = wager)
        return render_to_response('djeo/fj.html', {'fj':fj_object, 'fj_answer':fj_answer, 'contestant': contestant}, context_instance=RequestContext(request))  
    

    elif request.method == 'POST' and request.POST.get('answer'):
        answer = request.POST.get('answer')
        print answer
        total_cash = contestant.total_cash
        wager = contestant.wager
        #USER ANSWERED THIS QUESTION: ADD THAT ROW TO THE DB        
        if answer == fj_object.correct_answer:
            #CORRECT ANSWER
            Contestant.objects.filter(user=user).update(total_cash = total_cash + wager)
            contestant.total_cash = (total_cash + wager)
            Contestant.objects.filter(user=user).update(wager = 0)
            question = fj_object.id
            print "question id", question
            new_user_answer = UserAnswer(user=user, question=question, answered=1, correct=1)
            new_user_answer.save()
            return render_to_response('djeo/correct.html', {'contestant': contestant, 'fj':fj_object, 'fj_answer':fj_answer}, context_instance=RequestContext(request))
        else:
            #WRONG!
            if total_cash - wager <= 0:
                Contestant.objects.filter(user=user).update(total_cash = 25000)
                Contestant.objects.filter(user=user).update(wager = 0)
                wager = 0
            elif total_cash:
                Contestant.objects.filter(user=user).update(total_cash = total_cash - wager)
                contestant.total_cash = (total_cash - wager)
                Contestant.objects.filter(user=user).update(wager = 0)
                question = fj_object.id
                print "questoin id", question
                new_user_answer = UserAnswer(user=user, question=question, answered=1, correct=0)
                new_user_answer.save()

            return render_to_response('djeo/wrong.html', {'contestant': contestant, 'fj':fj_object, 'fj_answer':fj_answer}, context_instance=RequestContext(request))
    else:
        return render_to_response('djeo/play.html', {'fj':fj_object, 'fj_answer':fj_answer, 'contestant': contestant}, context_instance=RequestContext(request))
