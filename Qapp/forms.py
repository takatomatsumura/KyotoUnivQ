from django import forms
from .models import QuestionModel, AnswerModel, MessageModel, GoodModel, Profile
from django.contrib.auth.models import User
from django.contrib.auth import forms as auth_forms
from django.forms import ModelForm
from Accounts.models import CustomUser


class FindFormByWords(forms.Form):
	#検索ワード
	words = forms.CharField(label='words', required=False)

	#validation
	def clean_words(self):
		words = self.clean_data['words']
		if words == "None" :
			raise forms.ValidationError("無効な値が含まれています。")
		if "/" in words :
			raise forms.ValidationError("無効な値が含まれています。")

class ReportForm(forms.Form):
	CHOICE = [
		('1', '不適切な表現が含まれる。'),
		('2', '質問と解答の不一致')
		]
	choice = forms.ChoiceField(required=True, choices=CHOICE)

class BestAnswerSelectForm(forms.Form):
	#選択ボタンの設置
	select = forms.ChoiceField(label='選択', widget=forms.RadioSelect, choices = ['0', '選択'])

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['belong']

class AnswerForm(forms.ModelForm):
	class Meta:
		model = AnswerModel
		fields = ['content', 'image1', 'image2', 'image3']

class MessageForm(forms.ModelForm):
	class Meta:
		model = MessageModel
		fields = ['content']

class QuestionForm(forms.ModelForm):
	class Meta:
		model = QuestionModel
		fields = ['title', 'content', 'tag', 'image1', 'image2', 'image3']

class GoodForm(forms.ModelForm):
	class Meta:
		model = GoodModel
		fields = []

class UpdateImageForm(forms.ModelForm):
	class Mera:
		model = Profile
		fields = ['image']

class UpdateUsernameForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ['username']

class UpdateIntroForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['intro']

class UpdateHideForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['hide']

class ProfileSignupForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'belong', 'intro']

