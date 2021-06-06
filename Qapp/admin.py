from django.contrib import admin
from .models import QuestionModel, AnswerModel, GoodModel, MessageModel, Profile

# Register your models here.

admin.site.register(MessageModel)
admin.site.register(GoodModel)
admin.site.register(QuestionModel)
admin.site.register(AnswerModel)
admin.site.register(Profile)