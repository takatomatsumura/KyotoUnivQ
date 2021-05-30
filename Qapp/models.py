from django.db import models
from django.conf import settings
from Accounts.models import CustomUser

# Create your models here.

class QuestionModel(models.Model):
	#質問タイトル
	title = models.CharField(max_length=150)
	#質問内容
	content = models.CharField(max_length=1500)
	#投稿ユーザー
	post_user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name='post_user')
	#日付
	date = models.DateTimeField(auto_now_add=True)
	#添付画像
	image1 = models.ImageField(upload_to = '', blank=True, null=True)
	image2 = models.ImageField(upload_to = '', blank=True, null=True)
	image3 = models.ImageField(upload_to = '', blank=True, null=True)
	#タグ
	tag = models.ForeignKey(TagModel, on_delete=models.SET_NULL, null=True, related_name='tag')
	#状態 - False : 未解答, True : 解答済み
	condition = models.BooleanField(default=False)

	def __str__(self):
		return self.title.__str__()

class AnswerModel(models.Model):
	#解答したユーザー
	ans_user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = 'ans_user')
	#解答した質問
	question = models.ForeignKey(QuestionModel, on_delete = models.CASCADE, related_name = 'question')
	#解答内容
	content = models.CharField(max_length=1500)
	#ベストアンサー
	best = models.BooleanField(default=False)
	#添付画像
	image1 = models.ImageField(upload_to = '', blank=True, null=True)
	image2 = models.ImageField(upload_to = '', blank=True, null=True)
	image3 = models.ImageField(upload_to = '', blank=True, null=True)
	#日付
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.ans_user.username.__str__()

class MessageModel(models.Model):
	#メッセージが送信されている質問
	answer = models.ForeignKey(AnswerModel, on_delete = models.CASCADE, related_name = 'answer')
	#メッセージ内容
	content = models.CharField(max_length=200)
	#メッセージ送信ユーザー
	sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'sender')
	#日付
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.answer.__str__()