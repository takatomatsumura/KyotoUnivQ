from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError

class MyAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if not "@st.kyoto-u.ac.jp" in email:
            raise ValidationError('')
        return email