from django.contrib import admin
from .models import TagModel, QuestionModel, AnswerModel

# Register your models here.

admin.site.register(TagModel)
admin.site.register(QuestionModel)
admin.site.register(AnswerModel)