from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import QuestionModel, AnswerModel, TagModel
from .forms import FindFormByWords, MessageForm, ReportForm, AnswerForm, BestAnswerSelectForm, QuestionForm
from django.core.paginator import Paginator

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
        targets = targets.filter(condition = False)
    elif choose == "settled" :
        targets = targets.filter(condition = True)

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
        else:

            #<button name = "submit" value = "{{ answer.id  }}" -> Button for submitting MessageForm
            if (int)request.POST['submit'] > 0:
                form = MessageForm(request.POST)
                ans_num = (int)request.POST['submit']
                ans = AnswerModel.objects.get(pk = ans_num)

                form.instance.answer = ans
                form.instance.sender = request.user
                form.save()

                form = MessageForm()

            #<button name = "choice" value = "{{ answer.id }}" -> Button for Selecting The Best Answer
            elif (int)request.POST['choice'] > 0:
                selform = BestAnswerSelectForm(request.POST)
                sel_num = (int)request.POST['choice']
                sel = AnswerModel.objects.get(pk = sel_num)
                sel.best = True
                sel_q = QuestionModel.objects.get(answermodel_set__id = sel_num)
                sel_q.condition = True

    else:

        ansform = AnswerForm()
        selform = BestAnswerSelectForm()
        form = MessageForm()

    params = {
        "user" : request.user,
        "question" : question,
        "answers" : answers,
        "form" : form,
        "selform" : selform,
        "ansform" : ansform,
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

