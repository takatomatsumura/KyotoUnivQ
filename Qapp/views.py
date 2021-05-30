from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import QuestionModel, AnswerModel, TagModel, Profile
from django.core.paginator import Paginator
from Accounts.models import CustomUser
from django.contrib.auth.models import User
from .forms import (
    FindFormByWords, 
    MessageForm, 
    ReportForm, 
    AnswerForm, 
    BestAnswerSelectForm, 
    QuestionForm, 
    GoodForm, 
    ProfileForm,
    UpdateUsernameForm,
    UpdateIntroForm,
    UpdateImageForm,
    UpdateHideForm
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

    if request.method == 'POST':
        form = FindFormByWords(request.POST)
        message = "検索ワードを入力 : "

        if form.is_valid:
            search_words = request.POST['words']
            redirect_url = reverse('Qapp:find')
            parameters = urlencode(dict(choose = "all", searchwords = search_words))
            url = f'{redirect_url}?{parameters}'
            return redirect(url)
        else:
            message = "検索エラー : 検索に失敗しました。"

    else:
        form = FindFormByWords()

    return render(request, "Qapp/index.html", {"form" : form, "message" : message})


"""
------------------find function------------------------
>>>> This function corresponds to *Questions List Pages*
>>>> You can also use this when you search them by tags
>>>> {{ for item in page_obj }} -> item.title
>>>> choose can get only "all" "pending" "setteled"
-------------------------------------------------------
"""

def find(request, choose, num=1 , searchwords="False", tagged="False"):

    if search == "False" :
        targets = QuestionModel.objects.all().order_by('-date')
    else:
        targets = QuestionModel.objects.filter(title__icontains = searchwords).order_by('-date')

    if not tagged == "False" :
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
            redirect_url = reverse('Qapp:find')
            parameters = urlencode(dict(choose = "all", searchwords = search_words))
            url = f'{redirect_url}?{parameters}'
            return redirect(url)
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
    answers = question.answermodel_set.all().prefetch_related('answermodel_set')
    # Messages for Each Answer => {% for message in {{ answers.MessageModel_set.all() }} %}

    if request.method == 'POST':

        if "answer" in request.POST:

            # Check Answered or not
            # This check must also be contained by question.html.
            # When question is answered, the answer form should be hiden.

            answered = False

            for answer in answers:
                if answer.ans_user == request.user:
                    answered = True

            # Check end

            if not answered:
                ansform = AnswerForm(request.POST)
                ansform.instance.ans_user = request.user
                ansform.instance.question = question
                ansform.save()

        elif "search" in request.POST:
            form = FindFormByWords(request.POST)
            message = "検索ワードを入力 : "

            if form.is_valid:
                search_words = request.POST['words']
                redirect_url = reverse('Qapp:find')
                parameters = urlencode(dict(choose = "all", searchwords = search_words))
                url = f'{redirect_url}?{parameters}'
                return redirect(url)
            else:
                message = "検索エラー : 検索に失敗しました。"

        #<form><button name = "good" value = "{{ answer.id }}">
        elif "good" in request.POST:
            ans_num = (int)request.POST['good']
            ans = AnswerModel.objects.get(pk = ans_num)

            # Check whether already gooded or not
            if not ans.ans_user == request.user and not GoodModel.objects.filter(answer = ans, gooder = request.user).exists():
                goodform = GoodForm()
                goodform.answer = ans
                goodform.gooder = request.user
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
            ans_num = (int)request.POST['submit']
            ans = AnswerModel.objects.get(pk = ans_num)

            form.instance.answer = ans
            form.instance.sender = request.user
            form.save()

            form = MessageForm()

        #<button name = "choice" value = "{{ answer.id }}" -> Button for Selecting The Best Answer
        #Please check in the template file wheteher request.user == teh person who submit this question
        elif "choice" in request.POST:
            selform = BestAnswerSelectForm(request.POST)
            sel_num = (int)request.POST['choice']
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
def post(request):

    if request.method == 'POST':

        form = QuestionForm(request.POST)
        form.post_user = request.user
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

    if not User.objects.filter(pk = pk).exists():
        return render(request, "404.html")

    _user = User.objects.get(pk = pk)
    _user_profile = Profile.objects.get(pk = pk)
    rank = -1
    ranked_query = Profile.objects.all().order_by('-good_points')
    if request.user == profile :

        question_all = QuestionModel.object.filter(post_user = request.user)
        answer_all = AnswerModel.objects.filter(ans_user = request.user)
        ans_question_all = []
        for answer in answer_all:
            question = QuestionModel.objects.filter(answermodel_set = answer).first()
            ans_question_all.append(question)

        page_question = paginate_queryset(request, question_all, 5)
        page_ans_question = paginate_queryset(request, ans_question_all, 5)

        if request.method == 'POST':
            
            if "image" in request.POST:
                imageform = UpdateImageForm(request.POST, request.FILES)
                user_profile = Profile.objects.get(owner = request.user)
                user_profile.image = iamgeform.cleaned_data["image"]
                user_profile.save()

            if "username" in request.POST:
                nameform = UpdateUsernameForm(request.POST)
                user_obj = User.objects.get(username = request.user.username)
                user_obj.username = nameform.cleaned_data["username"]

            if "intro" in request.POST:
                introform = UpdateIntroForm(request.POST)
                user_profile = Profile.objects.get(owner = request.user)
                user_profile.intro = introform.cleaned_data["intro"]
                user_profile.save()

            if "hide" in request.POST:
                hideform = UpdateHideForm(request.POST)
                user_profile = Profile.objects.get(owner = request.user)
                user_profile.hide = introform.cleaned_data["hide"]
                user_profile.save()

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
            "page_question" : page_question,
            "page_ans_question" : page_ans_question,
        }

        return render(request, "profile.html", params)

    else:
        params = {
            "user_profile" : _user_profile,
            "user" : _user,
            }

        return render(request, "profile.html", params)

"""
-----------user_question_list function-----------------
>>>> This function corresponds to *User Questions List Pages*
>>>> You can also use this when you search them by tags
>>>> {{ for item in page_obj }} -> item.title
>>>> choose can get only "all" "pending" "setteled"
-------------------------------------------------------
"""
def user_question_list(request, choose):
    targets = QuestionModel.objects.filter(post_user = request.user)

    if choose == "pending" :
        targets = targets.filter(condition = "False")
    elif choose == "settled" :
        targets = targets.filter(condition = "True")

    page_obj = paginate_queryset(request, targets, 15)
    return render(request, "userquestion.html", {"search" : targets, "page_obj" : page_obj})


"""
-----------user_answer_list function-----------------
>>>> This function corresponds to *User Questions List Pages*
>>>> You can also use this when you search them by tags
>>>> {{ for item in page_obj }} -> item.title
>>>> choose can get only "all" "pending" "setteled"
-------------------------------------------------------
"""
def user_answer_list(request, choose):
    answer_all = AnswerModel.objects.filter(ans_user = request.user)
    ans_question_all = []
    for answer in answer_all:
        question = QuestionModel.objects.filter(answermodel_set = answer).first()
        ans_question_all.append(question)

    page_obj = paginate_queryset(request, ans_question_all, 15)
    return render(request, "userquestion.html", {"search" : ans_question_all, "page_obj" : page_obj})






























