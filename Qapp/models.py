from django.db import models
from django.conf import settings
from Accounts.models import CustomUser

# Create your models here.

CHOICE = (
	('総合人間学部', '総合人間学部'),
	('文学部', '文学部'),
	('教育学部', '教育学部'),
	('法学部', '法学部'),
	('経済学部', '経済学部'),
	('理学部', '理学部'),
	('医学部医学科', '医学部医学科'),
	('医学部人間健康学科', '医学部人間健康学科'),
	('薬学部', '薬学部'),
	('工学部地球工学科', '工学部地球工学科'),
	('工学部建築学科', '工学部建築学科'),
	('工学部物理工学科', '工学部物理工学科'),
	('工学部電気電子工学科', '工学部電気電子工学科'),
	('工学部情報学科', '工学部情報学科'),
	('工学部工業化学科', '工学部工業化学科'),
	('農学部資源生物科学科', '農学部資源生物科学科'),
	('農学部応用生命科学科', '農学部応用生命科学科'),
	('農学部地域環境工学科', '農学部地域環境工学科'),
	('農学部食料・環境経済学科', '農学部食料・環境経済学科'),
	('農学部森林科学科', '農学部森林科学科'),
	('農学部食品生物科学科', '農学部食品生物科学科'),
	('学校生活', '学校生活'),
	('全学共通科目', '全学共通科目'),
	)

class Profile(models.Model):
	CHOICE = (
	('総合人間学部', '総合人間学部'),
	('文学部', '文学部'),
	('教育学部', '教育学部'),
	('法学部', '法学部'),
	('経済学部', '経済学部'),
	('理学部', '理学部'),
	('医学部医学科', '医学部医学科'),
	('医学部人間健康学科', '医学部人間健康学科'),
	('薬学部', '薬学部'),
	('工学部地球工学科', '工学部地球工学科'),
	('工学部建築学科', '工学部建築学科'),
	('工学部物理工学科', '工学部物理工学科'),
	('工学部電気電子工学科', '工学部電気電子工学科'),
	('工学部情報学科', '工学部情報学科'),
	('工学部工業化学科', '工学部工業化学科'),
	('農学部資源生物科学科', '農学部資源生物科学科'),
	('農学部応用生命科学科', '農学部応用生命科学科'),
	('農学部地域環境工学科', '農学部地域環境工学科'),
	('農学部食料・環境経済学科', '農学部食料・環境経済学科'),
	('農学部森林科学科', '農学部森林科学科'),
	('農学部食品生物科学科', '農学部食品生物科学科'),
	)
	owner = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
	#いいね総数
	good_points = models.IntegerField(default=0)
	#所属学部、学科
	belong = models.CharField(max_length=50, choices=CHOICE)
	#称号
	degree = models.CharField(max_length=100, blank=True, null=True)
	#自己紹介
	intro = models.CharField(max_length=500, blank=True, null=True)
	#ユーザー画像
	image = models.ImageField(upload_to='', blank=True, null=True)
	#総いいね数のオン・オフ - True : オン（表示） False : オフ（非表示）
	hide = models.CharField(max_length=10, default="True", choices=(("True", "True"), ("False", "False")))

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
	tag = models.CharField(max_length=50, blank=True, null=True, choices=CHOICE)
	#状態 - False : 未解答, True : 解答済み
	condition = models.CharField(max_length=10,default="True", choices=(("True", "True"), ("False", "False")))

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
	models.CharField(default="False", choices=(("True", "True"), ("False", "False")))
	#添付画像
	image1 = models.ImageField(upload_to = '', blank=True, null=True)
	image2 = models.ImageField(upload_to = '', blank=True, null=True)
	image3 = models.ImageField(upload_to = '', blank=True, null=True)
	#日付
	date = models.DateTimeField(auto_now_add=True)
	#いいね
	good = models.IntegerField(default=0)

	def __str__(self):
		return self.ans_user.username.__str__()

class GoodModel(models.Model):
	answer = models.ForeignKey(AnswerModel, on_delete = models.CASCADE, related_name = 'ans_good')
	gooder = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = 'user_good')

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