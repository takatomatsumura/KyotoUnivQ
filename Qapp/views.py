from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import QuestionModel, AnswerModel, MessageModel, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator
from Accounts.models import CustomUser
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from .forms import (
    FindFormByWords, 
    MessageForm, 
    ReportForm, 
    AnswerForm, 
    BestAnswerSelectForm, 
    QuestionForm, 
    GoodForm, 
    ProfileSignupForm,
    UpdateUsernameForm,
    UpdateIntroForm,
    UpdateImageForm,
    UpdateHideForm
    )

CHOICE = (
    '総合人間学部',
    '文学部',
    '教育学部',
    '法学部',
    '経済学部',
    '理学部',
    '医学部医学科',
    '医学部人間健康学科',
    '薬学部',
    '工学部地球工学科',
    '工学部建築学科',
    '工学部物理工学科',
    '工学部電気電子工学科',
    '工学部情報学科',
    '工学部工業化学科',
    '農学部資源生物科学科',
    '農学部応用生命科学科',
    '農学部地域環境工学科',
    '農学部食料・環境経済学科',
    '農学部森林科学科',
    '農学部食品生物科学科',
    '学校生活',
    '全学共通科目',
    )

def paginate_queryset(request, queryset, count):
    """
    return Page Object
    count : objects per page
    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


"""
------------------index function-----------------------
>>>> This function corresponds to *Top Page*
-------------------------------------------------------
"""

def index(request):

    message = "検索ワードを入力 : "

    if request.method == 'POST':
        form = FindFormByWords(request.POST)

        if form.is_valid:
            search_words = request.POST['words']
            return redirect('Qapp:search', choose = "all", searchwords = search_words, tagged="notagged")
        else:
            message = "検索エラー : 検索に失敗しました。"

    else:
        form = FindFormByWords()

    settled_questions = QuestionModel.objects.filter(condition = "True").order_by('-date')

    return render(request, "Qapp/index.html", {"form" : form, "message" : message, 'questions' : settled_questions})


"""
------------------find function------------------------
>>>> This function corresponds to *Questions List Pages*
>>>> You can also use this when you search them by tags
>>>> {{ for item in page_obj }} -> item.title
>>>> choose can get only "all" "pending" "setteled"
-------------------------------------------------------
"""

def find(request, choose, searchwords, tagged):
    
    message = "検索ワードを入力 : "

    if searchwords == "False" :
        targets = QuestionModel.objects.all().order_by('-date')
    else:
        targets = QuestionModel.objects.filter(Q(title__icontains = searchwords)|Q(content__icontains = searchwords)).order_by('-date_settled')

    if not tagged == "notagged" :
        targets = targets.filter(tag = tagged)

    if choose == "pending" :
        targets = targets.filter(condition = "False")
    elif choose == "settled" :
        targets = targets.filter(condition = "True")

    if request.method == 'POST':
        form = FindFormByWords(request.POST)
        message = "検索ワードを入力 : "

        if form.is_valid:
            search_words = request.POST['words']
            return redirect('Qapp:search', choose = "all", searchwords = search_words, tagged="notagged")
        else:
            message = "検索エラー : 検索に失敗しました。"

    else:
        form = FindFormByWords()

    page_obj = paginate_queryset(request, targets, 15)
    return render(request, "Qapp/find.html", {"page_obj" : page_obj, "form" : form, "tagged" : tagged, "message" : message})

def findByTag(request, choose, tagged="notagged"):

    targets = QuestionModel.objects.all().order_by('-date')

    if not tagged == "notagged" :
        targets = targets.filter(tag = tagged)

    if not tagged in CHOICE:
        tagged = "notagged"

    if request.method == 'POST':
        form = FindFormByWords(request.POST)
        message = "検索ワードを入力 : "

        if form.is_valid:
            search_words = request.POST['words']
            return redirect('Qapp:search', choose = "all", searchwords = search_words, tagged="notagged")
        else:
            message = "検索エラー : 検索に失敗しました。"

    else:
        form = FindFormByWords()

    page_obj = paginate_queryset(request, targets, 15)
    return render(request, "Qapp/find.html", {"page_obj" : page_obj, "form" : form, "tagged" : tagged, "message" : message})


"""
----------------question function----------------------
>>>> This function corresponds to *Question Page*
>>>> This function requires the MessageForm submit button
>>>>      name the id/pk of the answer.
-------------------------------------------------------
"""
def question(request, num):

    question = QuestionModel.objects.get(pk = num)
    answers = AnswerModel.objects.filter(question = question)

    no_answered = True

    if question.condition == "True":
        no_answered = False
    else:
        for answer in answers:
            if answer.ans_user == request.user:
                no_answered = False

    if request.method == 'POST':

        if "answer" in request.POST:

            if not answered:
                ansform = AnswerForm(request.POST)
                ansform.instance.ans_user = request.user
                ansform.instance.question = question
                ansform.save()

        elif "search" in request.POST:
            findform = FindFormByWords(request.POST)
            message = "検索ワードを入力 : "

            if findform.is_valid:
                search_words = request.POST['words']
                return redirect('Qapp:search', choose = "all", searchwords = search_words, tagged="notagged")
            else:
                message = "検索エラー : 検索に失敗しました。"

        #<form><button name = "good" value = "{{ answer.id }}">
        elif "good" in request.POST:
            ans_num = int(request.POST['good'])
            ans = AnswerModel.objects.get(pk = ans_num)

            # Check whether already gooded or not
            if not ans.ans_user == request.user and not GoodModel.objects.filter(answer = ans, gooder = request.user).exists():
                goodform = GoodForm()
                goodform.instance.answer = ans
                goodform.instance.gooder = request.user
                goodform.save()
                ans.good += 1
                ans.save()
                ans.ans_user.good_points += 1
                ans.ans_user.save()

            else:
                gooded = GoodModel.objects.get(answer = ans, gooder = request.user)
                gooded.delete()
                ans.good -= 1
                ans.save()
                ans.ans_user.good_points -= 1
                ans.ans_user.save()

        #<button name = "submit" value = "{{ answer.id  }}"> -> Button for submitting MessageForm
        elif "submit" in request.POST:
            form = MessageForm(request.POST)
            ans_num = int(request.POST['submit'])
            ans = AnswerModel.objects.get(pk = ans_num)

            form.instance.answer = ans
            form.instance.sender = request.user
            form.save()

            form = MessageForm()

        #<button name = "choice" value = "{{ answer.id }}" -> Button for Selecting The Best Answer
        #Please check in the template file wheteher request.user == the person who submit this question
        elif "choice" in request.POST:
            selform = BestAnswerSelectForm(request.POST)
            sel_num = int(request.POST['choice'])
            sel = AnswerModel.objects.get(pk = sel_num)
            sel.best = "True"
            sel.save()
            sel_q = QuestionModel.objects.get(answermodel_set__id = sel_num)
            sel_q.condition = "True"
            sel_q.save()


    else:

        ansform = AnswerForm()
        selform = BestAnswerSelectForm()
        findform = FindFormByWords()
        form = MessageForm()

    params = {
        "user" : request.user,
        "question" : question,
        "answers" : answers,
        "form" : form,
        "selform" : selform,
        "ansform" : ansform,
        "findform" : findform,
        "no_answered" : no_answered,
    }

    return render(request, "Qapp/question.html", params)

"""
----------------report function----------------------
>>>> This function corresponds to *Report Page*
>>>> typed can get only "answer" "question"
-------------------------------------------------------
"""
def report(request, typed, pk):
    
    if request.method == 'POST':

        form = ReportForm(request.POST)
        print(typed)
        print(pk)
        print(request.POST)
        return redirect('/')

    else:

        form = ReportForm()

    return render(request, "Qapp/report.html", {'form' : form})

"""
---------------- Post function----------------------
>>>> This function corresponds to *Question-Post Page*
-------------------------------------------------------
"""
@login_required
def post(request):

    if request.method == 'POST':

        form = QuestionForm(request.POST)
        form.instance.post_user = request.user
        form.save()

    else:

        form = QuestionForm()

    return render(request, "Qapp/post.html", {'form' : form})

"""
----------------profile function----------------------
>>>> This function corresponds to *Profile Page*
-------------------------------------------------------
"""
def profile(request, pk):

    if not CustomUser.objects.filter(pk = pk).exists():
        return render(request, "Qapp/404.html")

    _user = CustomUser.objects.get(pk = pk)

    if not Profile.objects.filter(pk = pk).exists():
        return render(request, "Qapp/no_profile.html")

    _user_profile = Profile.objects.get(pk = pk)

    #True : the user's questions False : the user's answered questions
    now_selected = True

    if request.user == profile :

        question_all = QuestionModel.objects.filter(post_user = request.user)
        ans_question_all = QuestionModel.objects.filter(answermodel_set__ans_user = request.user)

        if request.method == 'POST':
            
            #<button name = "image" value = "value" -> Button for changing user image
            if "image" in request.POST:
                imageform = UpdateImageForm(request.POST, request.FILES)
                user_profile = Profile.objects.get(owner = request.user)
                user_profile.image = iamgeform.cleaned_data["image"]
                user_profile.save()

            #<button name = "username" value = "value" -> Button for changing username
            if "username" in request.POST:
                nameform = UpdateUsernameForm(request.POST)
                user_obj = User.objects.get(username = request.user.username)
                user_obj.username = nameform.cleaned_data["username"]

            #<button name = "intro" value = "value" -> Button for changing introduction
            if "intro" in request.POST:
                introform = UpdateIntroForm(request.POST)
                user_profile = Profile.objects.get(owner = request.user)
                user_profile.intro = introform.cleaned_data["intro"]
                user_profile.save()

            #<button name = "hide" value = "value" -> Button for hiding all Goods the user got 
            if "hide" in request.POST:
                hideform = UpdateHideForm(request.POST)
                user_profile = Profile.objects.get(owner = request.user)
                user_profile.hide = introform.cleaned_data["hide"]
                user_profile.save()

            #<button name = "change" value = "value" -> Button for Selecting whether to show answers or questions
            if "change" in request.POST:
                if now_selected :
                    now_selected = False
                else:
                    now_selected = True

        else:

            imageform = UpdateImageForm()
            nameform = UpdateUsernameForm()
            introform = UpdateIntroForm()

        params = {
            "imageform" : imageform,
            "nameform" : nameform,
            "introform" : introform,
            "user_profile" : _user_profile,
            "user" : _user,
            "questions" : question_all,
            "ans_questions" : ans_question_all,
            "now_selected" : now_selected,
            "requser" : request.user,
        }

        return render(request, "profile.html", params)

    else:
        params = {
            "user_profile" : _user_profile,
            "user" : _user,
            }

        return render(request, "Qapp/profile.html", params)

"""
----------------setting function----------------------
>>>> This function corresponds to *Setting Page*
-------------------------------------------------------
"""
def setting(request):
    # logout, password_change -> Accounts App
    return render(request, "Qapp/setting.html", {"user" : request.user})

def tag(request):
    return render(request, "Qapp/tag.html", {"choices" : CHOICE})

def next_signup(request):

     if request.method == 'POST':
         form = ProfileSignupForm(request.POST)
         form.instance.owner = request.user
         form.save()
         return redirect(to = '/')
     else:
         form = ProfileSignupForm()

     return render(request, "Qapp/next_signup.html", {"form" : form})
























